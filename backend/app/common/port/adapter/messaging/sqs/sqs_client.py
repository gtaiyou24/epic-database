import os
from typing import NoReturn

import boto3
from injector import inject, singleton


@singleton
class SQSClient:
    @inject
    def __init__(self, session: boto3.Session):
        self.__client = session.client('sqs',
                                       region_name=os.getenv('SQS_REGION_NAME', 'ap-northeast-1'),
                                       endpoint_url=os.getenv('SQS_ENDPOINT_URL'))
        self.__queue_url = os.getenv('SQS_QUEUE_URL')
        self.__receive_params = {
            'QueueUrl': self.__queue_url,
            'AttributeNames': ['All'],
            'MessageAttributeNames': ['All'],
            'MaxNumberOfMessages': 1,
            'VisibilityTimeout': 300,
            'WaitTimeSeconds': 10,
        }

    def receive_messages(self) -> list[dict]:
        messages: dict = self.__client.receive_message(**self.__receive_params)
        return messages.get('Messages', [])

    def delete_message(self, a_message: dict) -> NoReturn:
        self.__client.delete_message(QueueUrl=self.__queue_url, ReceiptHandle=a_message["ReceiptHandle"])
