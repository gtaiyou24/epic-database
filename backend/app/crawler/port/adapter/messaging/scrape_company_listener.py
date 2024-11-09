from typing import override

from di import DIContainer

from common.port.adapter.messaging import ExchangeListener
from crawler.application.company import ScrapeCompanyApplicationService


class ScrapeCompanyListener(ExchangeListener):
    def __init__(self):
        self.__scrape_company_application_service: ScrapeCompanyApplicationService | None = None

    @property
    def scrape_company_application_service(self) -> ScrapeCompanyApplicationService:
        self.__scrape_company_application_service = (
                self.__scrape_company_application_service
                or DIContainer.instance().resolve(ScrapeCompanyApplicationService)
        )
        return self.__scrape_company_application_service

    @override
    def filtered_dispatch(self, event_type: str, text_message: str) -> None:
        self.scrape_company_application_service.scrape_all()

    @override
    def publisher_name(self) -> str:
        return "scheduler"

    @override
    def listens_to(self, event_type: str) -> bool:
        return event_type in ["ScrapeCompany.1"]
