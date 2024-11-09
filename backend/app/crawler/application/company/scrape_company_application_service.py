import random
import time

from injector import inject
from slf4py import set_logger

from common.application import transactional
from crawler.domain.model.data import DataSet
from crawler.domain.model.extractor import DataSetExtractors, CssSelector, TableRowExtractor, XPathSelector
from crawler.domain.model.interim import InterimId, InterimRepository, Interim
from crawler.domain.model.page import PageService
from crawler.domain.model.scrape import ScrapeCompanyURLService
from crawler.domain.model.url import URL


@set_logger
class ScrapeCompanyApplicationService:
    @inject
    def __init__(self,
                 page_service: PageService,
                 interim_repository: InterimRepository):
        self.__page_service = page_service
        self.__interim_repository = interim_repository
        self.__dataset_extractors = {
            "https://houjin.jp/c/{}": DataSetExtractors([
                TableRowExtractor('company_url', 'URL'),
                TableRowExtractor('telephone', '電話番号'),
            ]),
            "https://salesnow.jp/db/companies/{}": DataSetExtractors([
                CssSelector('company_url', 'div.ProfileBox_link__MJT8n'),
                XPathSelector('market', '//*[@id="__next"]/div[1]/div[1]/div[1]/div[4]/div/div[1]/div[3]/div[4]/span/text()[2]'),
                XPathSelector('capital', '//*[@id="__next"]/div[1]/div[1]/div[2]/div[1]/div/div[1]/div[2]/div/div[3]/div[1]/div[2]/text()'),
            ]),
            "https://alarmbox.jp/companyinfo/entities/{}": DataSetExtractors([
                TableRowExtractor('company_url', 'URL'),
                TableRowExtractor('capital', '資本金'),
                TableRowExtractor('employee_number', '従業員数'),
                TableRowExtractor('telephone', '電話番号'),
                TableRowExtractor('market', '上場区分'),
                TableRowExtractor('ticker_symbol', '証券コード'),
            ]),
            "https://cnavi.g-search.or.jp/detail/{}.html": DataSetExtractors([
                TableRowExtractor('capital', '資本金'),
                TableRowExtractor('employee_number', '従業員数'),
            ]),
            "https://www.houjin.info/detail/{}/": DataSetExtractors([
                CssSelector('company_url', 'td > a[target="_blank"]'),
            ])
        }

    def scrape_all(self):
        for interim in self.__interim_repository.interims_with_source(Interim.Source.GBIZINFO):
            self.scrape(interim.get('corporate_number'))

    @transactional
    def scrape(self, corporate_number: str) -> None:
        id = InterimId.Type.JCN.make(corporate_number)
        interim = self.__interim_repository.get(id)

        # 他ウェブサイトから法人情報を取得する
        scraped: list[DataSet] = []
        for _url, dataset_extractors in self.__dataset_extractors.items():
            url = URL(_url.format(corporate_number))
            try:
                page = self.__page_service.fetch(url)
                dataset = dataset_extractors.extract(interim, page)
                scraped.append(dataset)
            except Exception as e:
                self.log.error(e)
                continue

        # 収集した法人情報をまとめる
        dataset = DataSet.concat(scraped)

        # TODO: 他Webサイトから事前に収集した情報(売上高,資金調達,...)と統合する

        if not interim.get('company_url'):
            # ホームページがない場合は、Google の検索結果を元にホームページを収集
            url = ScrapeCompanyURLService().scrape(interim)
            if url:
                interim.set('company_url', url.absolute)

        # TODO: ホームページから各情報を収集する

        interim = interim.set_with_dataset(dataset)

        self.__interim_repository.save(interim)
        time.sleep(int(random.uniform(3, 10)))
