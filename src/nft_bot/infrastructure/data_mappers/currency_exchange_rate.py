from decimal import Decimal
from typing import override

from aiohttp import ClientSession
from redis.asyncio import Redis

from nft_bot.application.currency_exchange_rate.data_gateway import (
    CurrencyExchangeRateDataGateway,
    CurrencyType,
)
from nft_bot.domain.nft.entity import (
    NftCryptoCurrencyType,
    NftCurrencyType,
)
from nft_bot.domain.nft.value_objects import NftExchangeRate, NftPrice

BASE_URL = (
    "https://cdn.jsdelivr.net/npm/"
    "@fawazahmed0/currency-api@latest"
    "/v1/currencies/{0}.json"
)
CURRENCIES = [_.value for _ in NftCryptoCurrencyType] + [
    _.value for _ in NftCurrencyType
]


class CurrencyExchangeRateDataMapper(CurrencyExchangeRateDataGateway):
    def __init__(
        self,
        connect: Redis,
        http_session: ClientSession,
    ) -> None:
        self._connect = connect
        self._http_session = http_session

    async def _get_exchange_rate(
        self,
        from_currency: CurrencyType,
        to_currency: CurrencyType,
    ) -> Decimal:
        async with self._http_session.get(
            BASE_URL.format(from_currency.value),
        ) as response:
            currencies: dict[str, float] = (await response.json())[
                from_currency.value
            ]
        for key, value in currencies.items():
            if key in CURRENCIES:
                await self._connect.set(
                    f"currency.from.{from_currency.value}.to.{key}",
                    str(value),
                    ex=3600,
                )
        return Decimal(currencies[to_currency.value])

    @override
    async def get_exchange_rate(
        self,
        from_currency: CurrencyType,
        to_currency: CurrencyType,
    ) -> NftExchangeRate:
        cache_data = await self._connect.get(
            f"currency.from.{from_currency.value}.to.{to_currency.value}",
        )
        if cache_data:
            return NftExchangeRate(Decimal(cache_data))

        result = await self._get_exchange_rate(
            from_currency=from_currency,
            to_currency=to_currency,
        )
        return NftExchangeRate(result)
