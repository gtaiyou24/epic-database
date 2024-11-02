import abc

from common.port.adapter.schedule import Scheduler


class ModuleBatch(abc.ABC):
    @property
    @abc.abstractmethod
    def schedulers(self) -> list[Scheduler]:
        pass

    @abc.abstractmethod
    def startup(self) -> None:
        pass

    @abc.abstractmethod
    def shutdown(self) -> None:
        pass

    def run(self, name: str, *args, **kwargs) -> None:
        for scheduler in self.schedulers:
            if scheduler.name == name:
                scheduler.run(*args, **kwargs)
