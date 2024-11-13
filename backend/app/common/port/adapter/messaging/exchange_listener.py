import abc


class ExchangeListener(abc.ABC):
    @abc.abstractmethod
    async def filtered_dispatch(self, event_type: str, text_message: str) -> None:
        """イベントタイプとメッセージ指定でメッセージを処理する"""
        pass

    @abc.abstractmethod
    def publisher_name(self) -> str:
        """購読するイベント発行元コンテキスト名を指定"""
        pass

    @abc.abstractmethod
    def listens_to(self, event_type: str) -> bool:
        """イベントタイプ指定で購読するイベントかどうかを判定する"""
        pass
