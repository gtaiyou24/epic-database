import asyncio
import random
import re
import time

from injector import inject
from slf4py import set_logger

from common.application import transactional
from crawler.domain.model.data import DataSet
from crawler.domain.model.extractor import DataSetExtractors, CssSelector, TableRowExtractor, XPathSelector, \
    DataExtractor
from crawler.domain.model.interim import InterimId, InterimRepository, Interim
from crawler.domain.model.page import PageService
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
                DataExtractor(TableRowExtractor('company_url', 'URL'), [
                    lambda value: value.strip(),
                    lambda value: value if re.match(r"^(https|http)?://[\w/:%#\$&\?\(\)~\.=\+\-]+", value) else None
                ]),
                DataExtractor(TableRowExtractor('telephone', '電話番号'), [
                    lambda value: value.replace('\n', '').replace('\t', '').strip(),
                    lambda value: str(value).replace('-', ''),
                    lambda value: value if re.match(r'[0-9]+', value) else None
                ]),
            ]),
            "https://salesnow.jp/db/companies/{}": DataSetExtractors([
                DataExtractor(
                    XPathSelector(
                        'company_url',
                        '//*[@id="__next"]/div[1]/div[1]/div[1]/div[4]/div/div[1]/div[3]/div[2]/div/text()'
                    ),
                    [
                        lambda value: value.strip(),
                        lambda value: value if re.match(r"^(https|http)?://[\w/:%#\$&\?\(\)~\.=\+\-]+", value) else None
                    ]
                ),
                DataExtractor(
                    XPathSelector(
                        'market',
                        '//*[@id="__next"]/div[1]/div[1]/div[1]/div[4]/div/div[1]/div[3]/div[4]/span/text()[2]'
                    ),
                    [
                        lambda value: value.replace('\n', '').replace('\t', '').strip(),
                        lambda value: value.replace('プライム（内国株式）', '東証プライム').replace(
                            'グロース（内国株式）', '東証グロース'
                        ).replace('スタンダード（内国株式）', '東証スタンダード').replace('PRO Market', 'Tokyo PRO')
                    ]
                ),
                DataExtractor(
                    XPathSelector(
                        'capital',
                        '//*[@id="__next"]/div[1]/div[1]/div[2]/div[1]/div/div[1]/div[2]/div/div[3]/div[1]/div[2]'
                        '/text()'
                    ),
                    [
                        lambda value: value.strip(),
                        lambda value: None if value == '-万円' else value
                    ]
                )
            ]),
            "https://alarmbox.jp/companyinfo/entities/{}": DataSetExtractors([
                DataExtractor(
                    TableRowExtractor('company_url', 'URL'),
                    [
                        lambda value: value.strip(),
                        lambda value: value if re.match(r"^(https|http)?://[\w/:%#\$&\?\(\)~\.=\+\-]+", value) else None
                    ]
                ),
                DataExtractor(
                    TableRowExtractor('capital', '資本金'),
                    [
                        lambda value: value.replace('\n', '').replace('\t', '').strip(),
                        lambda value: None if value == '-' else value
                    ]
                ),
                DataExtractor(
                    TableRowExtractor('employee_number', '従業員数'),
                    [
                        lambda value: value.replace('\n', '').replace('\t', '').strip(),
                        lambda value: None if value == '-' else value,
                        lambda value: int(value.replace('人', ''))
                    ]
                ),
                DataExtractor(
                    TableRowExtractor('telephone', '電話番号'),
                    [
                        lambda value: value.replace('\n', '').replace('\t', '').strip(),
                        lambda value: None if value == '-' else value,
                    ]
                ),
                DataExtractor(
                    TableRowExtractor('market', '上場区分'),
                    [
                        lambda value: value.replace('\n', '').replace('\t', '').strip(),
                    ]
                ),
            ]),
            "https://cnavi.g-search.or.jp/detail/{}.html": DataSetExtractors([
                DataExtractor(
                    TableRowExtractor('capital', '資本金'),
                    [
                        lambda value: value.replace('\n', '').replace('\t', '').strip(),
                        lambda value: None if value == '－' else value,
                    ]
                ),
                DataExtractor(
                    TableRowExtractor('employee_number', '従業員数'),
                    [
                        lambda value: value.replace('\n', '').replace('\t', '').strip(),
                        lambda value: None if value == '－' or not re.match('[0-9]+人', value) else value,
                        lambda value: int(value.replace('人', ''))
                    ]
                )
            ]),
            "https://www.houjin.info/detail/{}/": DataSetExtractors([
                DataExtractor(
                    CssSelector('company_url', 'td > a[target="_blank"]'),
                    [
                        lambda value: value.replace('\n', '').replace('\t', '').strip(),
                        lambda value: value if re.match(r"^(https|http)?://[\w/:%#\$&\?\(\)~\.=\+\-]+", value) else None
                    ]
                )
            ])
        }

    def scrape_all(self):
        for interim in self.__interim_repository.interims_with_source(Interim.Source.GBIZINFO):
            try:
                self.scrape(interim.get('corporate_number'))
            except Exception as e:
                self.log.error(e)
                continue

    @transactional
    def scrape(self, corporate_number: str) -> None:
        id = InterimId.Type.JCN.make(corporate_number)
        interim = self.__interim_repository.get(id)

        if interim is None:
            return

        # 他ウェブサイトから法人情報を取得する
        scraped: list[DataSet] = []
        for _url, dataset_extractors in self.__dataset_extractors.items():
            url = URL(_url.format(corporate_number))
            try:
                page = self.__page_service.fetch(url)
                dataset = asyncio.run(dataset_extractors.extract(interim, page))
                scraped.append(dataset)
            except Exception as e:
                self.log.error(e)
                continue

        # 収集した法人情報をまとめる
        dataset = DataSet.concat(scraped)
        interim = interim.set_with_dataset(dataset)

        self.log.info(f"{corporate_number}: {dataset.to_dict()}")

        # TODO: 他Webサイトから事前に収集した情報(売上高,資金調達,...)と統合する

        # if not interim.get('company_url'):
        #     ホームページがない場合は、Google の検索結果を元にホームページを収集
        #     url = ScrapeCompanyURLService().scrape(interim)
        #     if url:
        #        interim.set('company_url', url.absolute)

        # ホームページから各情報を収集する
        if interim.get('company_url'):
            page = self.__page_service.fetch(URL(interim.get('company_url')))
            if page.http_status.is_(200):
                ogp = page.to_beautiful_soup().find('meta', property='og:image')
                if ogp and ogp.get('content'):
                    image_url = URL.of(ogp.get('content'), page.url)
                    interim = interim.set('company_image', image_url.absolute)
                    self.log.info(f"company_image: {image_url.absolute}")

        self.__interim_repository.save(interim)
        time.sleep(int(random.uniform(3, 5)))
