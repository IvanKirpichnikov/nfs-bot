from collections.abc import Iterable
from datetime import datetime
from typing import Any, Final, cast, override

from adaptix import Retort, as_is_loader, loader
from psycopg import AsyncConnection

from nft_bot.application.nft.data_gateway import NftDataGateway
from nft_bot.application.nft.data_structure import (
    CreateNftGatewayDs,
    CurrencyTypeAndPriceDs,
    NftPaginateFromProfileGatewayDs,
    UpdateNftGatewayDs,
)
from nft_bot.application.nft.errors import NotFoundNftError
from nft_bot.domain.nft.entity import Nft, NftId
from nft_bot.domain.nft.value_objects import NftDescription, NftName, NftPrice
from nft_bot.domain.profile.entity import ProfileId

retort = Retort(
    recipe=[
        as_is_loader(datetime),
        loader(NftName, NftName),
        loader(NftPrice, NftPrice),
        loader(NftDescription, NftDescription),
    ],
)
CREATE_QUERY: Final = """
INSERT INTO nft(
    profile_id,
    name,
    file_id,
    price,
    currency,
    crypto_currency,
    description
)
VALUES(%s, %s, %s, %s, %s, %s, %s);
"""
PAGINATE_FROM_PROFILE_QUERY: Final = """
SELECT
    id,
    profile_id,
    name,
    price,
    file_id,
    description,
    currency,
    crypto_currency,
    created_at
FROM nft
WHERE profile_id = %s
ORDER BY id
OFFSET %s
LIMIT %s;
"""
READ_QUERY: Final = """
SELECT
    id,
    profile_id,
    name,
    price,
    file_id,
    description,
    currency,
    crypto_currency,
    created_at
FROM nft
WHERE id = %s
"""
UPDATE_QUERY: Final = """
UPDATE nft
SET description = COALESCE(%s, description)
WHERE id = %s;
"""
READ_TOTAL_COUNT_QUERY: Final = """
SELECT COUNT(*)
FROM nft
WHERE profile_id = %s;
"""
READ_CURRENCY_TYPES_AND_PRICES: Final = """
SELECT
    SUM(price) AS price,
    currency
FROM nft
WHERE profile_id = %s
GROUP BY currency;
"""


class NftDataMapper(NftDataGateway):
    def __init__(
        self,
        connection: AsyncConnection[Any],
    ) -> None:
        self._connection = connection

    @override
    async def create(self, data: CreateNftGatewayDs) -> None:
        await self._connection.execute(
            query=CREATE_QUERY,
            params=(
                data.profile_id,
                data.name,
                data.file_id,
                data.price,
                data.currency.value,
                data.crypto_currency.value,
                data.description,
            ),
        )

    @override
    async def paginate_from_profile(
        self,
        data: NftPaginateFromProfileGatewayDs,
    ) -> Iterable[Nft]:
        cursor = await self._connection.execute(
            query=PAGINATE_FROM_PROFILE_QUERY,
            params=(data.profile_id, data.offset, data.limit),
        )
        return retort.load(await cursor.fetchall(), list[Nft])

    @override
    async def read_total_count(self, data: ProfileId) -> int:
        cursor = await self._connection.execute(
            query=READ_TOTAL_COUNT_QUERY,
            params=(data,),
        )
        fetchone = await cursor.fetchone()
        if fetchone is None:
            return 0
        return cast(int, fetchone["count"])

    @override
    async def read(self, data: NftId) -> Nft:
        cursor = await self._connection.execute(
            query=READ_QUERY,
            params=(data,),
        )
        fetchone = await cursor.fetchone()
        if fetchone is None:
            raise NotFoundNftError("By id %s" % data)
        return retort.load(fetchone, Nft)

    @override
    async def update(self, data: UpdateNftGatewayDs) -> None:
        await self._connection.execute(
            query=UPDATE_QUERY,
            params=(data.description, data.id),
        )

    @override
    async def read_currencies_and_prices(
        self,
        data: ProfileId,
    ) -> Iterable[CurrencyTypeAndPriceDs]:
        cursor = await self._connection.execute(
            query=READ_CURRENCY_TYPES_AND_PRICES,
            params=(data,),
        )
        fetchone = await cursor.fetchall()
        return retort.load(fetchone, list[CurrencyTypeAndPriceDs])
