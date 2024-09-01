from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any, override

from psycopg import AsyncConnection

from nft_bot.application.common.transaction_manager import TransactionManager


class DatabaseTransactionManager(TransactionManager):
    def __init__(
        self,
        connection: AsyncConnection,
    ) -> None:
        self._connection = connection

    @asynccontextmanager
    @override
    async def __call__(self) -> AsyncIterator[Any]:
        async with self._connection.transaction():
            yield None
