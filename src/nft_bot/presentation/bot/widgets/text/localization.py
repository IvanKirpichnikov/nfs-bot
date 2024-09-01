from typing import Any, override

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.common import WhenCondition
from aiogram_dialog.widgets.text import Text
from dishka import FromDishka

from nft_bot.main.injects import aiogram_dialog_inject
from nft_bot.presentation.localization import Localization


class LocalizationText(Text):
    __slots__ = ["key"]

    @override
    def __init__(
        self,
        key: str,
        when: WhenCondition = None,
    ) -> None:
        super().__init__(when)
        self.key = key

    @aiogram_dialog_inject
    @override
    async def _render_text(
        self,
        data: dict[str, Any],
        manager: DialogManager,
        localization: FromDishka[Localization],
    ) -> str:
        return localization(
            self.key.format_map(data),
            **data.get("localization", {}),
        )
