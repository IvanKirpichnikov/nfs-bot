from abc import abstractmethod
from contextlib import AbstractAsyncContextManager
from typing import Any, Protocol


class TransactionManager(Protocol):
    @abstractmethod
    def __call__(self) -> AbstractAsyncContextManager[Any]:
        raise NotImplementedError
