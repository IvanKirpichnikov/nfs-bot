from collections.abc import MutableMapping
from typing import override

from cachetools import LRUCache

from nft_bot.application.common.id_provider import IdProvider
from nft_bot.application.profile.data_gateway import ProfileDataGateway
from nft_bot.domain.profile.entity import ProfileId, TgUserId
from nft_bot.presentation.bot.types import TelegramUser


class ProfileIdProvider(IdProvider[ProfileId]):
    _cache: MutableMapping[TgUserId, ProfileId] = LRUCache(maxsize=10_000)

    def __init__(
        self,
        telegram_user: TelegramUser,
        data_gateway: ProfileDataGateway,
    ) -> None:
        self._data_gateway = data_gateway
        self._tg_user_id = telegram_user.id

    @override
    async def __call__(self) -> ProfileId:
        cache_data = self._cache.get(self._tg_user_id)
        if cache_data:
            return cache_data
        profile = await self._data_gateway.read(self._tg_user_id)
        self._cache[self._tg_user_id] = profile.id
        return profile.id
