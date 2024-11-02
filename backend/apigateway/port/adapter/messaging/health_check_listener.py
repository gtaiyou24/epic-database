from typing import override

from slf4py import set_logger

from common.port.adapter.messaging import ExchangeListener


@set_logger
class HealthCheckListener(ExchangeListener):
    @override
    def filtered_dispatch(self, event_type: str, text_message: str) -> None:
        print(event_type, text_message)

    @override
    def publisher_name(self) -> str:
        return 'api-gateway'

    @override
    def listens_to(self, event_type: str) -> bool:
        return event_type == 'HealthCheck.1'
