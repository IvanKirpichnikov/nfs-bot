from typing import Any

from aiogram.enums import ContentType
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import Dialog, DialogManager, ShowMode, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Cancel, ManagedRadio, Radio
from aiogram_dialog.widgets.text import Const

from nft_bot.application.profile.data_gateway import ProfileDataGateway
from nft_bot.application.profile.interactors.update import (
    UpdateProfileInDs,
    UpdateProfileInteractor,
)
from nft_bot.domain.profile.entity import ProfileCurrencyType
from nft_bot.domain.profile.errors import ProfileNameError
from nft_bot.main.injects import aiogram_dialog_inject
from nft_bot.presentation.bot.states import SettingStates
from nft_bot.presentation.bot.types import TelegramUser
from nft_bot.presentation.bot.utils import get_widget
from nft_bot.presentation.bot.widgets.text.localization import LocalizationText
from nft_bot.presentation.localization import Localization


@aiogram_dialog_inject
async def on_start(
    data: Any,
    manager: DialogManager,
    *,
    telegram_user: TelegramUser,
    gateway: ProfileDataGateway,
) -> None:
    profile = await gateway.read(telegram_user.id)
    currency_type_widget: ManagedRadio[str] = get_widget(
        dialog_manager=manager,
        widget_id="currency_type",
    )
    await currency_type_widget.set_checked(profile.currency_type.value)


@aiogram_dialog_inject
async def message_process(
    event: Message,
    widget: MessageInput,
    manager: DialogManager,
    *,
    interactor: UpdateProfileInteractor,
) -> None:
    if event.text:
        await interactor(
            UpdateProfileInDs(
                name=event.text,
            ),
        )
        manager.show_mode = ShowMode.EDIT
    else:
        manager.show_mode = ShowMode.NO_UPDATE
    await event.delete()


@aiogram_dialog_inject
async def getter(
    dialog_manager: DialogManager,
    *,
    telegram_user: TelegramUser,
    localization: Localization,
    gateway: ProfileDataGateway,
    **kwargs: Any,
) -> dict[str, Any]:
    profile = await gateway.read(telegram_user.id)
    return {
        "localization": {
            "name": profile.name.name,
            "currency": localization(
                f"currency-{profile.currency_type.value}",
            ),
        },
    }


@aiogram_dialog_inject
async def currency_type_process(
    update: CallbackQuery,
    widget: ManagedRadio[str],
    manager: DialogManager,
    data: str,
    *,
    interactor: UpdateProfileInteractor,
) -> None:
    if widget.is_checked(data):
        return None

    await interactor(
        UpdateProfileInDs(
            currency_type=ProfileCurrencyType(data),
        ),
    )


dialog = Dialog(
    Window(
        LocalizationText("settings-menu"),
        MessageInput(
            func=message_process,
            content_types=ContentType.TEXT,
            filter=lambda event: ProfileNameError(event.text),
        ),
        Radio(
            Const("✅") + LocalizationText("currency-{item}"),
            LocalizationText("currency-{item}"),
            id="currency_type",
            item_id_getter=lambda x: x,
            on_click=currency_type_process,
            items=[_.value for _ in ProfileCurrencyType],
        ),
        Cancel(
            LocalizationText("back"),
            id="back",
            show_mode=ShowMode.DELETE_AND_SEND,
        ),
        getter=getter,
        state=SettingStates.main,
    ),
    on_start=on_start,
)
