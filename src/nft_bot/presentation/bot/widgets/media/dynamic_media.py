from collections.abc import Callable
from typing import Any, cast, override

from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import MediaAttachment
from aiogram_dialog.widgets.common import WhenCondition
from aiogram_dialog.widgets.media import Media

type MediaSelectorFunc = Callable[
    [dict[Any, Any]],
    MediaAttachment | None,
]
type MediaSelector = str | MediaAttachment | MediaSelectorFunc


class FixedDynamicMedia(Media):
    selector_func: MediaSelectorFunc

    @override
    def __init__(
        self,
        selector: MediaSelector,
        when: WhenCondition = None,
    ) -> None:
        super().__init__(when=when)
        if isinstance(selector, str):
            self.selector_func = lambda data: data.get(selector)
        elif isinstance(selector, MediaAttachment):
            self.selector_func = cast(MediaSelectorFunc, lambda data: selector)
        else:
            self.selector_func = cast(MediaSelectorFunc, selector)

    @override
    async def _render_media(
        self,
        data: dict[Any, Any],
        manager: DialogManager,
    ) -> MediaAttachment | None:
        return self.selector_func(data)
