import json
import threading
import time
from typing import NoReturn

from injector import singleton
from slf4py import set_logger

from common.exception import SystemException
from common.port.adapter.messaging import ExchangeListener
from common.port.adapter.messaging.sqs import SQSClient


@set_logger
@singleton
class SQSMessageConsumer:
    def __init__(self, sqs_client: SQSClient, exchange_listeners: set[ExchangeListener]):
        self.exchange_listeners = exchange_listeners
        self.sqs_client = sqs_client
        self.is_running = True

    def start_receiving(self) -> NoReturn:
        self.log.info('start receiving message!')

        def run() -> NoReturn:
            while self.is_running:
                messages = self.sqs_client.receive_messages()
                if messages:
                    self.log.info('dispatch message!')
                    for message in messages:
                        try:
                            self.dispatch_message(message['Body'])
                        except Exception as e:
                            self.log.error(e)
                        else:
                            self.sqs_client.delete_message(message)
                            self.log.info('message is subscribed!')
                else:
                    time.sleep(5)

        receiver_thread = threading.Thread(target=run)
        receiver_thread.start()

    def stop_receiving(self) -> NoReturn:
        self.log.info('stop receiving')
        self.is_running = False

    def dispatch_message(self, message: str) -> NoReturn:
        producer_name = eval(message)['producer_name']
        event_type = eval(message)['event_type']
        event = json.dumps(eval(message)['event'])

        for listener in self.exchange_listeners:
            if listener.producer_name == producer_name and listener.listens_to(event_type):
                try:
                    listener.filtered_dispatch(event_type, event)
                except SystemException as e:
                    e.logging()
                except Exception as e:
                    self.log.warn(e)
