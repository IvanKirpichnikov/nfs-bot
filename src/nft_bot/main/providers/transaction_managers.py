from typing import Any

from dishka import Provider, Scope, provide
from psycopg import AsyncConnection

from nft_bot.infrastructure.transaction_managers.database import (
    DatabaseTransactionManager,
)


class TransactionManagersProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def database(
        self,
        connection: AsyncConnection[Any],
    ) -> DatabaseTransactionManager:
        return DatabaseTransactionManager(connection)
