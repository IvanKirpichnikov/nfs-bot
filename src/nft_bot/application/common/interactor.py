from abc import abstractmethod
from typing import Protocol


class Interactor[InDs, OutDs](Protocol):
    @abstractmethod
    async def __call__(self, data: InDs) -> OutDs:
        raise NotImplementedError
