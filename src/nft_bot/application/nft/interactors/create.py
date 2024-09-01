from dataclasses import dataclass
from decimal import Decimal
from typing import override

from nft_bot.application.common.id_provider import IdProvider
from nft_bot.application.common.interactor import Interactor
from nft_bot.application.common.transaction_manager import TransactionManager
from nft_bot.application.nft.data_gateway import NftDataGateway
from nft_bot.application.nft.data_structure import CreateNftGatewayDs
from nft_bot.domain.nft.entity import NftCryptoCurrencyType, NftCurrencyType
from nft_bot.domain.nft.value_objects import NftDescription, NftName, NftPrice
from nft_bot.domain.profile.entity import ProfileId


@dataclass(frozen=True, slots=True)
class CreateNftInDs:
    name: str
    price: Decimal
    file_id: str
    currency: NftCurrencyType
    crypto_currency: NftCryptoCurrencyType
    description: str | None = None


@dataclass(frozen=True, slots=True)
class CreateNftInteractor(Interactor[CreateNftInDs, None]):
    data_gateway: NftDataGateway
    profile_id_provider: IdProvider[ProfileId]
    gateway_transaction_manager: TransactionManager

    @override
    async def __call__(self, data: CreateNftInDs) -> None:
        async with self.gateway_transaction_manager():
            await self.data_gateway.create(
                CreateNftGatewayDs(
                    profile_id=await self.profile_id_provider(),
                    file_id=data.file_id,
                    name=NftName(data.name).name,
                    price=NftPrice(data.price).price,
                    currency=data.currency,
                    crypto_currency=data.crypto_currency,
                    description=NftDescription(data.description).description,
                ),
            )
