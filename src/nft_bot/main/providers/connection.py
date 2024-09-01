from collections.abc import AsyncIterable, AsyncIterator
from typing import Any

from aiohttp import ClientSession
from dishka import Provider, Scope, provide
from psycopg import AsyncConnection
from psycopg.rows import dict_row
from psycopg_pool import AsyncConnectionPool
from redis.asyncio import Redis

from nft_bot.config import DatabaseConfig, RedisConfig


class ConnectionProvider(Provider):
    scope = Scope.APP

    @provide
    async def db_pool(
        self,
        config: DatabaseConfig,
    ) -> AsyncIterator[AsyncConnectionPool[AsyncConnection[Any]]]:
        async with AsyncConnectionPool(
            conninfo=config.url,
            max_size=config.pool_size,
            connection_class=AsyncConnection[Any],
        ) as pool:
            yield pool

    @provide(scope=Scope.REQUEST)
    async def db_connection(
        self,
        pool: AsyncConnectionPool[AsyncConnection[Any]],
    ) -> AsyncIterable[AsyncConnection[Any]]:
        async with pool.connection() as connection:
            connection.row_factory = dict_row
            yield connection

    @provide
    async def redis_connection(
        self,
        config: RedisConfig,
    ) -> AsyncIterable[Redis]:
        async with Redis.from_url(
            url=config.url,
            decode_responses=True,
        ) as redis:
            yield redis

    @provide
    async def http_session(self) -> AsyncIterable[ClientSession]:
        async with ClientSession() as http_session:
            yield http_session
