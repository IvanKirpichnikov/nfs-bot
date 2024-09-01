from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import NewType

from nft_bot.domain.nft.value_objects import NftDescription, NftName, NftPrice
from nft_bot.domain.profile.entity import ProfileId

NftId = NewType("NftId", int)


class NftCryptoCurrencyType(Enum):
    TRON = "trx"
    SOLANA = "sol"
    Ethereum = "eth"


class NftCurrencyType(Enum):
    USD = "usd"
    RUB = "rub"


@dataclass(frozen=True, slots=True)
class Nft:
    id: NftId
    profile_id: ProfileId
    file_id: str
    name: NftName
    price: NftPrice
    created_at: datetime
    currency: NftCurrencyType
    description: NftDescription
    crypto_currency: NftCryptoCurrencyType
