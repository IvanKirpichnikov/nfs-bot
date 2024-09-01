from collections.abc import Awaitable, Callable
from typing import Any, Protocol

from nft_bot.domain.profile.entity import TgChatId, TgUserId

type TelegramHandler[_EventType] = Callable[
    [_EventType, dict[str, Any]],
    Awaitable[Any],
]


class TelegramUser(Protocol):
    id: TgUserId
    full_name: str


class TelegramChat(Protocol):
    id: TgChatId
