import argparse

from slf4py import set_logger

from apigateway import apigateway
from authority import authority
from common import common
from common.port.adapter.messaging import ExchangeListener
from crawler import crawler
from listing import listing
from payment import payment


@set_logger
class Batch:
    def __init__(self, subscribers: set[ExchangeListener]):
        self._subscribers = subscribers

    def startup(self) -> None:
        common.startup()
        apigateway.startup()
        authority.startup()
        crawler.startup()
        listing.startup()
        payment.startup()

    def run(self, module: str, event_type: str, *args) -> None:
        for subscriber in self._subscribers:
            if subscriber.publisher_name() == module and subscriber.listens_to(event_type):
                subscriber.filtered_dispatch(event_type, '')

    def shutdown(self) -> None:
        common.shutdown()
        apigateway.shutdown()
        authority.shutdown()
        crawler.shutdown()
        listing.shutdown()
        payment.shutdown()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Batch')
    parser.add_argument("module", type=str, help="モジュール名を指定してください。")
    parser.add_argument("name", type=str, help="バッチ名を指定してください。")

    args = parser.parse_args()

    print("Module:", args.module)
    print("Name:", args.name)

    all_subscribers = set()
    for module in [common, apigateway, authority, crawler, listing, payment]:
        for subscriber in module.subscribers:
            all_subscribers.add(subscriber)

    batch = Batch(all_subscribers)
    try:
        batch.startup()
        batch.run(args.module, args.name)
    except Exception as e:
        print(e)
    finally:
        batch.shutdown()
