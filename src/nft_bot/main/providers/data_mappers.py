from dishka import Provider, Scope, provide

from nft_bot.application.currency_exchange_rate.data_gateway import (
    CurrencyExchangeRateDataGateway,
)
from nft_bot.application.nft.data_gateway import NftDataGateway
from nft_bot.application.profile.data_gateway import ProfileDataGateway
from nft_bot.infrastructure.data_mappers.currency_exchange_rate import (
    CurrencyExchangeRateDataMapper,
)
from nft_bot.infrastructure.data_mappers.nft import NftDataMapper
from nft_bot.infrastructure.data_mappers.profile import ProfileDataMapper


class DataMappersProvider(Provider):
    scope = Scope.REQUEST

    provides = (
        provide(NftDataMapper, provides=NftDataGateway)
        + provide(ProfileDataMapper, provides=ProfileDataGateway)
        + provide(
            CurrencyExchangeRateDataMapper,
            provides=CurrencyExchangeRateDataGateway,
        )
    )
