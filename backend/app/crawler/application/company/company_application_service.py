import io
import json
import zipfile
from datetime import date, datetime
from typing import TypedDict, Literal, Any

import fake_useragent
import requests
from cachecontrol import CacheControl
from cachecontrol.caches import FileCache
from injector import singleton, inject
from slf4py import set_logger

from common.application import transactional
from common.exception import SystemException, ErrorCode
from crawler.domain.model.listing import ListingManagementService
from crawler.domain.model.interim import InterimRepository, Interim, InterimId
from crawler.domain.model.url import URLSet, URL


class HojinInfoJson(TypedDict):
    """https://info.gbiz.go.jp/hojin/swagger-ui/index.html#/gBizINFO%20REST%20API/get"""
    corporate_number: str  # 法人番号
    name: str | None  # 法人名
    name_en: str | None  # 法人名英語
    kana: str | None  # 法人名フリガナ
    postal_code: str | None  # 郵便番号
    location: str | None  # 本社所在地(都道府県+市町村+番地/建物)
    representative_position: str | None  # 法人代表者役職
    representative_name: str | None  # 法人代表者名

    founding_year: int | None  # 創業年
    date_of_establishment: date | None  # 設立年月日
    business_summary: str | None  # 事業概要
    employee_number: int  # 従業員数
    capital_stock: int | None  # 資本金
    company_size_female: int | None  # 従業員数の内、女性が占める人数
    company_size_male: int | None  # 従業員数の内、男性が占める人数
    company_url: str | None  # 企業ホームページ

    # 登記記録の閉鎖等の事由(01: 清算の結了, 11: 合併による解散, 21: 登記官による閉鎖, 31: その他の清算の結了)
    close_cause: Literal["01", "11", "21", "31"] | None
    close_date: date | None  # 登記記録の閉鎖等年月日
    status: Literal["閉鎖", "-"]  # ステータス
    update_date: datetime  # 最終更新日

    number_of_activity: str | None  # 法人活動情報件数
    qualification_grade: str | None  # 全省庁統一資格の資格等級(物品の製造、物品の販売、役務の提供等、物品の買受け)

    business_items: Any | None
    qualification_grade: Any | None
    subsidy: Any | None


@singleton
@set_logger
class CompanyApplicationService:
    @inject
    def __init__(self,
                 dataset_service: ListingManagementService,
                 interim_repository: InterimRepository):
        self.__dataset_service = dataset_service
        self.__interim_repository = interim_repository
        self.__cached_session = CacheControl(requests.Session(), cache=FileCache('.webcache'))

    def download(self) -> None:
        """gBizINFO から法人データを一括ダウンロードする"""
        self.log.info("gBizINFO から法人データをダウンロード中...")

        response = self.__cached_session.post(
            'https://info.gbiz.go.jp/hojin/DownloadJson',
            headers={
                'Content-Type': 'application/json',
                'Referer': 'https://info.gbiz.go.jp/hojin/DownloadTop',
                'User-Agent': fake_useragent.UserAgent().random
            }
        )
        if not response.ok:
            raise SystemException(ErrorCode.DOWNLOAD_DATA_FAILED, "gBizINFO から法人データをダウンロードするのに失敗しました")

        self.log.info("ダウンロード完了!!")

        self.log.info("法人データを保存します...")
        with zipfile.ZipFile(io.BytesIO(response.content)) as zf:
            for path in zf.namelist():
                with zf.open(path) as f:
                    hojin_list: list[HojinInfoJson] = json.loads(f.read())
                    for hojin in hojin_list:
                        try:
                            self.save(hojin)
                        except Exception as e:
                            self.log.error(f"法人 {hojin.get('name')} でエラーが発生しました : {e}")

        self.log.info("法人データの保存完了!!")

    @transactional
    def save(self, payload: HojinInfoJson) -> None:
        corporate_number = InterimId.Type.JCN.make(payload.get('corporate_number'))
        interim_company = self.__interim_repository.get(corporate_number)
        if interim_company is not None:
            # すでに保存されている場合はスキップする
            self.log.info(f"法人 {payload.get('name')} はすでに保存されているため、スキップします")
            return

        # 法人データを新規作成する
        uuid = self.__interim_repository.next_identity()
        interim_company = Interim(
            uuid.set_other_id(corporate_number),
            Interim.Source.GBIZINFO,
            URLSet(set()),
            payload
        )

        self.__interim_repository.save(interim_company)

        self.log.info(f"法人 {payload.get('name')} を保存しました")

    def transfer(self) -> None:
        """データを連携する"""
        for interim in self.__interim_repository.interims_with_source(Interim.Source.GBIZINFO):
            self.__dataset_service.transfer('company', interim)
