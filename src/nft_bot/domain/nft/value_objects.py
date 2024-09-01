from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from nft_bot.domain.nft.errors import (
    NftDescriptionLengthError,
    NftNameLengthError,
    NftPriceError,
)


@dataclass(slots=True, frozen=True)
class NftName:
    name: str
    
    def __post_init__(self) -> None:
        len_value = len(self.name)
        if len_value > 25:
            msg = f"Name length {len_value} > 25"
            raise NftNameLengthError(msg, len_value)


@dataclass(slots=True, frozen=True)
class NftDescription:
    description: str | None
    
    def __post_init__(self) -> None:
        if self.description is None:
            return None
        
        len_value = len(self.description)
        if len_value > 400:
            msg = f"Description length {len_value} > 400"
            raise NftDescriptionLengthError(msg, len_value)


@dataclass(slots=True, frozen=True)
class NftPrice:
    price: Decimal
    
    def __post_init__(self) -> None:
        if self.price > 1_000_000:
            msg = f"Price({self.price}) > 1000000"
            raise NftPriceError(msg, self.price)
        if self.price < 1:
            msg = f"Price({self.price}) < 1"
            raise NftPriceError(msg, self.price)


@dataclass(slots=True, frozen=True)
class NftExchangeRate:
    price: Decimal
    
    def exchange(self, other: NftPrice) -> NftExchangeRate:
        return NftExchangeRate(self.price * other.price)
