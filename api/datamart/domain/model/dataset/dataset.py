from dataclasses import dataclass

from datamart.domain.model.dataset import Data


@dataclass(init=True, frozen=True)
class Dataset:
    set: list[Data]

    def __iter__(self):
        yield from self.set
