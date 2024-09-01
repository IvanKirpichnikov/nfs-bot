from typing import Any, override

from aiogram import BaseMiddleware, Bot
from aiogram.types import TelegramObject
from dishka.async_container import AsyncContainer

from nft_bot.main.injects import CONTAINER_KEY
from nft_bot.presentation.bot.types import (
    TelegramChat,
    TelegramHandler,
    TelegramUser,
)


def make_context(data: dict[str, Any]) -> dict[Any, Any]:
    values = [
        (Bot, "bot"),
        (TelegramObject, "event"),
        (TelegramChat, "event_chat"),
        (TelegramUser, "event_from_user"),
    ]
    return {value[0]: data[value[1]] for value in values if data.get(value[1])}


class ContainerMiddleware(BaseMiddleware):
    def __init__(self, container: AsyncContainer) -> None:
        self._container = container

    @override
    async def __call__(
        self,
        handler: TelegramHandler[TelegramObject],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        async with self._container(context=make_context(data)) as container:
            data[CONTAINER_KEY] = container
            return await handler(event, data)
