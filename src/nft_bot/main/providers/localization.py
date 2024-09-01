from dishka import Provider, Scope, provide

from nft_bot.presentation.localization import (
    Language,
    Localization,
    LocalizationStorage,
)


class LocalizationProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def localization(self, storage: LocalizationStorage) -> Localization:
        return storage.get_locale(Language.RU)
