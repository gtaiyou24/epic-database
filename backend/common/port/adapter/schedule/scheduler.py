import abc


class Scheduler(abc.ABC):
    """ジョブ実行クラス"""
    @abc.abstractmethod
    def name(self) -> str:
        """ジョブの名前"""
        pass

    @abc.abstractmethod
    def run(self, *args, **kwargs) -> None:
        """ジョブの実行処理"""
        pass
