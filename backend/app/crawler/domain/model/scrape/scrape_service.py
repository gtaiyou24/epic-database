import abc
import random
import time
from typing import override, Any

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service as ChromeService

from crawler.domain.model.interim import Interim
from crawler.domain.model.url import URL


class ScrapeService(abc.ABC):
    @abc.abstractmethod
    def scrape(self, interim: Interim) -> Any:
        pass


class ScrapeCompanyURLService(ScrapeService):
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # ヘッドレスモード
        options.add_argument("--disable-gpu")  # 暫定的に必要なフラグ
        options.add_argument('--lang=ja-JP')  # 日本語対応
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--disable-extensions")  # すべての拡張機能を無効にする
        options.add_argument("--disable-dev-tools")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-zygote")
        options.add_argument('--single-process')
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-setuid-sandbox")
        options.add_argument("--start-maximized")  # 最小画面で起動
        self.__browser = webdriver.Chrome(
            service=ChromeService(''),
            options=options
        )

    @override
    def scrape(self, interim: Interim) -> URL | None:
        # Google で検索し、検索結果を元にホームページを取得
        if interim.get('location'):
            keyword = f'"{interim.get('name')}" {interim.get('location')}'
        elif interim.get('postal_code'):
            keyword = f'"{interim.get('name')}" {interim.get('postal_code')}'
        else:
            keyword = f'"{interim.get('name')}"'

        self.__browser.get("https://google.com")

        search_box = WebDriverWait(self.__browser, 10)\
            .until(EC.visibility_of_element_located((By.NAME, "q")))
        search_box.send_keys(keyword)
        search_box.submit()

        time.sleep(random.randint(3, 10))

        for element in self.__browser.find_elements(By.XPATH, '//a/h3'):
            print(element.text)
            a = element.find_element(By.XPATH, '..')
            href = a.get_attribute("href")
            if href is not None:
                self.__browser.quit()
                return URL(href)

        self.__browser.quit()
        return None

        # beautiful_soup = page.to_beautiful_soup()
        # if beautiful_soup.select_one('#search') is None:
        #     a = beautiful_soup.find('a')
        #     if a.text == 'ここをクリック':
        #         page = self.__page_service.fetch(URL(f"https://www.google.co.jp{a.get('href')}"))
        #         beautiful_soup = page.to_beautiful_soup()
        #         print(page.url, beautiful_soup.text)
        #
        # print(f'===================================== {interim.get('corporate_number')}/{interim.get('name')} =====================================')
        # try:
        #     for a in beautiful_soup.select_one('#search').find_all('a'):
        #         href = a.get('href', None)
        #         if href is not None and href != '#':
        #             print(href)
        #             # interim.set('company_url', url)
        #             # break
        # except:
        #     print(beautiful_soup.text)
