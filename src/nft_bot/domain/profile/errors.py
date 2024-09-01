from nft_bot.domain.common.error import DomainError


class ProfileNameError(DomainError, ValueError):
    pass
