from abc import abstractmethod
from typing import Protocol


class IdProvider[OutputDataStructure_co](Protocol):
    @abstractmethod
    async def __call__(self) -> OutputDataStructure_co:
        raise NotImplementedError
