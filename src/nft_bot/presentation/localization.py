from __future__ import annotations

import os
from collections.abc import Mapping
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Any, Final, TYPE_CHECKING

from fluent.runtime import FluentLocalization, FluentResourceLoader


if TYPE_CHECKING:
    from nft_bot.config import LocalizationConfig

LOCALIZATION_NONE: Final = "None"
LOCALIZATION_VOID: Final = ""
type LocalizationKwargs = str | int | datetime | Decimal


class Language(Enum):
    RU = "ru"


class Localization:
    __slots__ = ["_source"]
    
    def __init__(self, source: FluentLocalization) -> None:
        self._source = source
    
    def __call__(self, key: str, /, **kwargs: LocalizationKwargs) -> str:
        text = self._source.format_value(key, kwargs)
        if text == key:
            raise ValueError("Not found text. Key: %r" % key)
        return text


class LocalizationStorage:
    __slots__ = (
        "_locales",
        "_default_language",
    )
    
    def __init__(
        self,
        locales: Mapping[Language, Localization],
        default_language: Language,
    ) -> None:
        self._locales = locales
        self._default_language = default_language
    
    def get_locale(self, language: Any) -> Localization:
        if isinstance(language, Language):
            language_ = language
        else:
            try:
                language_ = Language(language)
            except ValueError:
                language_ = self._default_language
        return self._locales[language_]


def build_localization_storage(
    config: LocalizationConfig,
) -> LocalizationStorage:
    locales = {}
    for language in Language:
        path = config.path / language.value
        locales[language] = Localization(
            FluentLocalization(
                locales=[language.value],
                resource_loader=FluentResourceLoader(str(path)),
                resource_ids=[
                    file for file in os.listdir(path) if file.endswith(".ftl")
                ],
            ),
        )
    
    return LocalizationStorage(
        locales=locales,
        default_language=config.default_language,
    )
