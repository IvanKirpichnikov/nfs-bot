from dishka import Provider, Scope, provide

from nft_bot.config import (
    Config,
    DatabaseConfig,
    LocalizationConfig,
    RedisConfig,
    TelegramBotConfig,
    TelegramBotOwnerConfig,
)


class ConfigProvider(Provider):
    scope = Scope.APP

    @provide
    def database(self, config: Config) -> DatabaseConfig:
        return config.database

    @provide
    def redis(self, config: Config) -> RedisConfig:
        return config.redis

    @provide
    def telegram_bot(self, config: Config) -> TelegramBotConfig:
        return config.telegram_bot

    @provide
    def telegram_bot_owner(
        self,
        config: TelegramBotConfig,
    ) -> TelegramBotOwnerConfig:
        return config.owner

    @provide
    def localization(self, config: Config) -> LocalizationConfig:
        return config.localization
