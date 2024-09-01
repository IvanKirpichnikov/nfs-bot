from dataclasses import dataclass

from nft_bot.domain.profile.errors import ProfileNameError


@dataclass(slots=True, frozen=True)
class ProfileName:
    name: str

    def __post_init__(self) -> None:
        len_value = len(self.name)
        if len_value > 25:
            msg = f"Name length {len_value} > 25"
            raise ProfileNameError(msg)
