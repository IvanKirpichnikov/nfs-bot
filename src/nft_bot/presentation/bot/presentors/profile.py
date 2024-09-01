from typing import Any

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import Dialog, DialogManager, ShowMode, StartMode, Window
from aiogram_dialog.widgets.kbd import Button, Start, Url
from aiogram_dialog.widgets.text import Format

from nft_bot.application.profile.interactors.create import (
    CreateProfileInDs,
    CreateProfileInteractor,
)
from nft_bot.application.profile.interactors.read import (
    ReadProfileDataInteractor,
)
from nft_bot.config import TelegramBotOwnerConfig
from nft_bot.domain.profile.entity import ProfileCurrencyType
from nft_bot.main.injects import aiogram_dialog_inject, aiogram_handler_inject
from nft_bot.presentation.bot.states import (
    AddNftStates,
    PaginationNftStates,
    ProfileStates,
    SettingStates,
)
from nft_bot.presentation.bot.types import TelegramChat, TelegramUser
from nft_bot.presentation.bot.widgets.text.localization import LocalizationText
from nft_bot.presentation.localization import Localization


@aiogram_dialog_inject
async def getter(
    *,
    localization: Localization,
    telegram_user: TelegramUser,
    config: TelegramBotOwnerConfig,
    interactor: ReadProfileDataInteractor,
    **kwargs: Any,
) -> dict[str, Any]:
    data = await interactor(telegram_user.id)
    return {
        "contact_administration": config.url,
        "localization": {
            "name": data.name,
            "total_price": data.total_price,
            "currency_type": data.currency_type.value,
            "currency": localization(f"currency-{data.currency_type.value}"),
        },
    }


async def to_pagination_nft(
    update: CallbackQuery,
    widget: Button,
    manager: DialogManager,
) -> None:
    await manager.start(
        show_mode=ShowMode.EDIT,
        state=PaginationNftStates.main,
    )


dialog = Dialog(
    Window(
        LocalizationText("profile-menu"),
        Button(
            LocalizationText("my-nft"),
            id="pagination_nft",
            on_click=to_pagination_nft,
        ),
        Start(
            LocalizationText("add-nft"),
            id="add_nft",
            show_mode=ShowMode.EDIT,
            state=AddNftStates.main,
        ),
        Start(
            LocalizationText("settings"),
            id="settings",
            show_mode=ShowMode.EDIT,
            state=SettingStates.main,
        ),
        Url(
            LocalizationText("contact-administration"),
            Format("{contact_administration}"),
        ),
        getter=getter,
        state=ProfileStates.main,
    ),
)


@aiogram_handler_inject
async def start_profile(
    update: Message,
    dialog_manager: DialogManager,
    *,
    telegram_user: TelegramUser,
    telegram_chat: TelegramChat,
    interactor: CreateProfileInteractor,
) -> None:
    await interactor(
        CreateProfileInDs(
            name=telegram_user.full_name,
            tg_chat_id=telegram_chat.id,
            tg_user_id=telegram_user.id,
            currency_type=ProfileCurrencyType.RUB,
        ),
    )
    await dialog_manager.start(
        state=ProfileStates.main,
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.DELETE_AND_SEND,
    )
