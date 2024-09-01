from dishka import Provider, Scope, from_context

from nft_bot.config import Config
from nft_bot.presentation.bot.types import TelegramUser
from nft_bot.presentation.localization import (
    LocalizationStorage,
)


class ContextProvider(Provider):
    provides = (
        from_context(Config, scope=Scope.APP)
        + from_context(LocalizationStorage, scope=Scope.APP)
        + from_context(TelegramUser, scope=Scope.REQUEST)
    )
