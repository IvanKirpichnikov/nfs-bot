from decimal import Decimal

from nft_bot.domain.common.error import DomainError


class NftNameLengthError(DomainError, ValueError):
    def __init__(self, msg: str, length: int) -> None:
        super().__init__(msg)
        self.length = length


class NftDescriptionLengthError(DomainError, ValueError):
    def __init__(self, msg: str, length: int) -> None:
        super().__init__(msg)
        self.length = length


class NftPriceError(DomainError, ValueError):
    def __init__(self, msg: str, length: Decimal) -> None:
        super().__init__(msg)
        self.length = length
