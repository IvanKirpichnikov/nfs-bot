import tomllib
from dataclasses import dataclass, field
from pathlib import Path

from adaptix import Retort

from nft_bot.domain.profile.entity import TgChatId, TgUserId
from nft_bot.presentation.localization import Language

retort = Retort()


@dataclass(slots=True, frozen=True)
class TelegramBotOwnerConfig:
    url: str
    tg_user_id: TgUserId
    tg_chat_id: TgChatId


@dataclass(slots=True, frozen=True)
class TelegramBotConfig:
    token: str = field(repr=False)
    user_name: str
    skip_updates: bool
    storage_url: str
    owner: TelegramBotOwnerConfig


@dataclass(frozen=True, slots=True)
class DatabaseConfig:
    url: str
    pool_size: int


@dataclass(frozen=True, slots=True)
class RedisConfig:
    url: str


@dataclass(frozen=True, slots=True)
class LocalizationConfig:
    path: Path
    default_language: Language


@dataclass(frozen=True, slots=True)
class Config:
    database: DatabaseConfig
    redis: RedisConfig
    telegram_bot: TelegramBotConfig
    localization: LocalizationConfig


def build_config(path: Path) -> Config:
    with path.open("rb") as file:
        raw_data = tomllib.load(file)
    return retort.load(raw_data, Config)
