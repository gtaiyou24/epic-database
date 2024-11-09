from typing import override

import fake_useragent
import requests

from crawler.domain.model.page import Page, HttpStatus
from crawler.domain.model.page.html import Html, CharacterCode
from crawler.domain.model.url import URL
from crawler.port.adapter.service.page.adapter import SearchEngineAdapter


class GoogleAdapter(SearchEngineAdapter):
    @override
    def search(self, keyword: str) -> Page:
        response = requests.get(
            f'https://www.google.co.jp/search?q={keyword}',
            headers={
                'Accept-Language': 'ja',
                'User-Agent': fake_useragent.UserAgent().random
            }
        )
        return Page(
            url=URL(response.url),
            html=Html(
                content=response.text,
                character_code=CharacterCode.value_of(response.apparent_encoding),
            ),
            http_status=HttpStatus.value_of(response.status_code),
        )

    @override
    def fetch(self, url: URL) -> Page:
        user_agent = fake_useragent.UserAgent().random
        response = requests.get(url.absolute, headers={'Accept-Language': 'ja', 'User-Agent': user_agent})
        return Page(
            url=URL(response.url),
            html=Html(
                content=response.text,
                character_code=CharacterCode.value_of(response.apparent_encoding),
            ),
            http_status=HttpStatus.value_of(response.status_code),
        )
