from dataclasses import dataclass
from typing import override

from nft_bot.application.common.interactor import Interactor
from nft_bot.application.common.transaction_manager import TransactionManager
from nft_bot.application.nft.data_gateway import NftDataGateway
from nft_bot.application.nft.data_structure import UpdateNftGatewayDs
from nft_bot.domain.nft.entity import NftId
from nft_bot.domain.nft.value_objects import NftDescription


@dataclass(frozen=True, slots=True)
class UpdateNftInDs:
    id: NftId
    description: str | None = None


@dataclass(frozen=True, slots=True)
class UpdateNftInteractor(Interactor[UpdateNftInDs, None]):
    data_gateway: NftDataGateway
    gateway_transaction_manager: TransactionManager

    @override
    async def __call__(self, data: UpdateNftInDs) -> None:
        async with self.gateway_transaction_manager():
            await self.data_gateway.update(
                UpdateNftGatewayDs(
                    id=data.id,
                    description=NftDescription(data.description).description,
                ),
            )
