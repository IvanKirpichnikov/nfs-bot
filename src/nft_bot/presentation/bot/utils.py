from typing import Any, cast

from aiogram_dialog import DialogManager
from aiogram_dialog.api.internal import Widget


def get_start_data(
    manager: DialogManager,
) -> dict[str, Any]:
    return cast(
        dict[str, Any],
        manager.start_data,
    )


def get_widget(
    dialog_manager: DialogManager,
    widget_id: str,
) -> Any:
    widget = dialog_manager.find(widget_id=widget_id)
    if widget is None:
        raise ValueError(
            "Not found aiogram dialog widget by widget_id %r" % widget_id,
        )
    return cast(Widget, widget)


def calculate_number_pages(total_count: int, limit: int) -> int:
    return total_count // limit + bool(total_count % limit)
