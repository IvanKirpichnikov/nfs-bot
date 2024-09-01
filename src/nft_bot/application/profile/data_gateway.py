from abc import abstractmethod
from typing import Protocol

from nft_bot.application.profile.data_structure import (
    CreateProfileGatewayDs,
    UpdateProfileGatewayDs,
)
from nft_bot.domain.profile.entity import Profile, TgUserId


class ProfileDataGateway(Protocol):
    @abstractmethod
    async def create(self, data: CreateProfileGatewayDs) -> None:
        raise NotImplementedError

    @abstractmethod
    async def read(self, data: TgUserId) -> Profile:
        raise NotImplementedError

    @abstractmethod
    async def exists(self, data: TgUserId) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def update(self, data: UpdateProfileGatewayDs) -> None:
        raise NotImplementedError
