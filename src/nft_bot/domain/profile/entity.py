from dataclasses import dataclass
from enum import Enum
from typing import NewType

from nft_bot.domain.profile.value_objects import ProfileName

ProfileId = NewType("ProfileId", int)
TgChatId = NewType("TgChatId", int)
TgUserId = NewType("TgUserId", int)


class ProfileCurrencyType(Enum):
    USD = "usd"
    RUB = "rub"


@dataclass(frozen=True, slots=True)
class Profile:
    id: ProfileId
    name: ProfileName
    currency_type: ProfileCurrencyType
    tg_user_id: TgUserId
    tg_chat_id: TgChatId
