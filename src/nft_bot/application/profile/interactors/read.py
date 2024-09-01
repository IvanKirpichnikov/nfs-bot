from dataclasses import dataclass
from decimal import Decimal
from typing import override

from nft_bot.application.common.interactor import Interactor
from nft_bot.application.currency_exchange_rate.data_gateway import (
    CurrencyExchangeRateDataGateway,
)
from nft_bot.application.nft.data_gateway import NftDataGateway
from nft_bot.application.profile.data_gateway import ProfileDataGateway
from nft_bot.consts import ZERO_DECIMAL
from nft_bot.domain.profile.entity import (
    ProfileCurrencyType,
    TgUserId,
)


@dataclass(frozen=True, slots=True)
class ReadProfileDataOutDs:
    name: str
    total_price: Decimal
    currency_type: ProfileCurrencyType


@dataclass(frozen=True, slots=True)
class ReadProfileDataInteractor(Interactor[TgUserId, ReadProfileDataOutDs]):
    nft_data_gateway: NftDataGateway
    profile_data_gateway: ProfileDataGateway
    currency_data_gateway: CurrencyExchangeRateDataGateway
    
    @override
    async def __call__(self, data: TgUserId) -> ReadProfileDataOutDs:
        profile = await self.profile_data_gateway.read(data)
        currencies_and_prices = (
            await self.nft_data_gateway.read_currencies_and_prices(
                profile.id,
            )
        )
        total_price = ZERO_DECIMAL
        for currency_and_price in currencies_and_prices:
            exchange_rate = await self.currency_data_gateway.get_exchange_rate(
                to_currency=profile.currency_type,
                from_currency=currency_and_price.currency,
            )
            total_price += exchange_rate.exchange(
                currency_and_price.price
            ).price
        
        return ReadProfileDataOutDs(
            name=profile.name.name,
            total_price=total_price,
            currency_type=profile.currency_type,
        )
