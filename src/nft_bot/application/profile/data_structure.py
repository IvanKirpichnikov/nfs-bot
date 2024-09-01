from dataclasses import dataclass

from nft_bot.domain.profile.entity import (
    ProfileCurrencyType,
    ProfileId,
    TgChatId,
    TgUserId,
)


@dataclass(frozen=True, slots=True)
class CreateProfileGatewayDs:
    name: str
    tg_user_id: TgUserId
    tg_chat_id: TgChatId
    currency_type: ProfileCurrencyType


@dataclass(frozen=True, slots=True)
class UpdateProfileGatewayDs:
    id: ProfileId
    name: str | None = None
    currency_type: ProfileCurrencyType | None = None
