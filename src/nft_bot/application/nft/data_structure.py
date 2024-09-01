from dataclasses import dataclass
from decimal import Decimal

from nft_bot.domain.nft.entity import (
    NftCryptoCurrencyType,
    NftCurrencyType,
    NftId,
)
from nft_bot.domain.nft.value_objects import NftPrice
from nft_bot.domain.profile.entity import ProfileId


@dataclass(frozen=True, slots=True)
class CreateNftGatewayDs:
    profile_id: ProfileId
    name: str
    file_id: str
    price: Decimal
    currency: NftCurrencyType
    crypto_currency: NftCryptoCurrencyType
    description: str | None = None


@dataclass(frozen=True, slots=True)
class UpdateNftGatewayDs:
    id: NftId
    description: str | None = None


@dataclass(frozen=True, slots=True)
class NftPaginateFromProfileGatewayDs:
    profile_id: ProfileId
    offset: int
    limit: int


@dataclass(frozen=True, slots=True)
class CurrencyTypeAndPriceDs:
    price: NftPrice
    currency: NftCurrencyType
