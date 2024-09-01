from abc import abstractmethod
from collections.abc import Iterable
from typing import Protocol

from nft_bot.application.nft.data_structure import (
    CreateNftGatewayDs,
    CurrencyTypeAndPriceDs,
    NftPaginateFromProfileGatewayDs,
    UpdateNftGatewayDs,
)
from nft_bot.domain.nft.entity import Nft, NftId
from nft_bot.domain.profile.entity import ProfileId


class NftDataGateway(Protocol):
    @abstractmethod
    async def create(self, data: CreateNftGatewayDs) -> None:
        raise NotImplementedError

    @abstractmethod
    async def paginate_from_profile(
        self,
        data: NftPaginateFromProfileGatewayDs,
    ) -> Iterable[Nft]:
        raise NotImplementedError

    @abstractmethod
    async def read_total_count(self, data: ProfileId) -> int:
        raise NotImplementedError

    @abstractmethod
    async def read(self, data: NftId) -> Nft:
        raise NotImplementedError

    @abstractmethod
    async def update(self, data: UpdateNftGatewayDs) -> None:
        raise NotImplementedError

    @abstractmethod
    async def read_currencies_and_prices(
        self,
        data: ProfileId,
    ) -> Iterable[CurrencyTypeAndPriceDs]:
        raise NotImplementedError
