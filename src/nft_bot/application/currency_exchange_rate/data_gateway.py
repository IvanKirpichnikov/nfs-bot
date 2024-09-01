from abc import abstractmethod
from typing import Protocol

from nft_bot.domain.nft.entity import (
    NftCryptoCurrencyType,
    NftCurrencyType,
)
from nft_bot.domain.nft.value_objects import NftExchangeRate, NftPrice
from nft_bot.domain.profile.entity import ProfileCurrencyType

type CurrencyType = (
    NftCurrencyType | NftCryptoCurrencyType | ProfileCurrencyType
)


class CurrencyExchangeRateDataGateway(Protocol):
    @abstractmethod
    async def get_exchange_rate(
        self,
        from_currency: CurrencyType,
        to_currency: CurrencyType,
    ) -> NftExchangeRate:
        raise NotImplementedError
