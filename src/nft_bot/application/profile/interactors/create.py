from dataclasses import dataclass
from typing import ClassVar, override

from nft_bot.application.common.interactor import Interactor
from nft_bot.application.common.transaction_manager import TransactionManager
from nft_bot.application.profile.data_gateway import ProfileDataGateway
from nft_bot.application.profile.data_structure import CreateProfileGatewayDs
from nft_bot.domain.profile.entity import (
    ProfileCurrencyType,
    TgChatId,
    TgUserId,
)
from nft_bot.domain.profile.value_objects import ProfileName


@dataclass(frozen=True, slots=True)
class CreateProfileInDs:
    name: str
    tg_user_id: TgUserId
    tg_chat_id: TgChatId
    currency_type: ProfileCurrencyType


@dataclass(frozen=True, slots=True)
class CreateProfileInteractor(Interactor[CreateProfileInDs, None]):
    data_gateway: ProfileDataGateway
    gateway_transaction_manager: TransactionManager

    _cache: ClassVar[dict[TgUserId, None]] = {}

    @override
    async def __call__(self, data: CreateProfileInDs) -> None:
        if data.tg_user_id in self._cache:
            return None

        async with self.gateway_transaction_manager():
            exists = await self.data_gateway.exists(data.tg_user_id)
            if exists:
                self._cache[data.tg_user_id] = None
                return None

            await self.data_gateway.create(
                CreateProfileGatewayDs(
                    tg_user_id=data.tg_user_id,
                    tg_chat_id=data.tg_chat_id,
                    currency_type=data.currency_type,
                    name=ProfileName(data.name).name,
                ),
            )
