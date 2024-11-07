from typing import override

from di import DIContainer

from common.port.adapter.messaging import ExchangeListener
from crawler.application.company import CompanyApplicationService


class TransferCompanyListener(ExchangeListener):
    def __init__(self):
        self.__company_application_service: CompanyApplicationService | None = None

    @property
    def company_application_service(self) -> CompanyApplicationService:
        self.__company_application_service = (
            self.__company_application_service or DIContainer.instance().resolve(CompanyApplicationService)
        )
        return self.__company_application_service

    @override
    def filtered_dispatch(self, event_type: str, text_message: str) -> None:
        self.company_application_service.transfer()

    @override
    def publisher_name(self) -> str:
        return "scheduler"

    @override
    def listens_to(self, event_type: str) -> bool:
        return event_type in ["TransferCompany.1"]
