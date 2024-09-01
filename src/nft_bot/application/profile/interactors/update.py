from dataclasses import dataclass
from typing import override

from nft_bot.application.common.id_provider import IdProvider
from nft_bot.application.common.interactor import Interactor
from nft_bot.application.common.transaction_manager import TransactionManager
from nft_bot.application.profile.data_gateway import ProfileDataGateway
from nft_bot.application.profile.data_structure import (
    UpdateProfileGatewayDs,
)
from nft_bot.domain.profile.entity import ProfileCurrencyType, ProfileId
from nft_bot.domain.profile.value_objects import ProfileName


@dataclass(frozen=True, slots=True)
class UpdateProfileInDs:
    name: str | None = None
    currency_type: ProfileCurrencyType | None = None


@dataclass(frozen=True, slots=True)
class UpdateProfileInteractor(Interactor[UpdateProfileInDs, None]):
    data_gateway: ProfileDataGateway
    profile_id_provider: IdProvider[ProfileId]
    gateway_transaction_manager: TransactionManager

    @override
    async def __call__(self, data: UpdateProfileInDs) -> None:
        async with self.gateway_transaction_manager():
            await self.data_gateway.update(
                UpdateProfileGatewayDs(
                    id=await self.profile_id_provider(),
                    currency_type=data.currency_type,
                    name=ProfileName(
                        data.name,
                    ).name
                    if data.name
                    else None,
                ),
            )
