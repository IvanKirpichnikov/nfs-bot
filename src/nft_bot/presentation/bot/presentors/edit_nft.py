from typing import Any

from aiogram.enums import ContentType
from aiogram.types import Message
from aiogram_dialog import Dialog, DialogManager, ShowMode, Window
from aiogram_dialog.api.entities import MediaAttachment, MediaId
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Cancel

from nft_bot.application.currency_exchange_rate.data_gateway import (
    CurrencyExchangeRateDataGateway,
)
from nft_bot.application.nft.data_gateway import NftDataGateway
from nft_bot.application.nft.interactors.update import (
    UpdateNftInDs,
    UpdateNftInteractor,
)
from nft_bot.domain.nft.entity import NftId
from nft_bot.domain.nft.errors import NftDescriptionLengthError
from nft_bot.domain.nft.value_objects import NftDescription
from nft_bot.main.injects import aiogram_dialog_inject
from nft_bot.presentation.bot.states import EditNftStates
from nft_bot.presentation.bot.widgets.media.dynamic_media import (
    FixedDynamicMedia,
)
from nft_bot.presentation.bot.widgets.text.localization import LocalizationText
from nft_bot.presentation.localization import LOCALIZATION_VOID, Localization


async def on_start(
    start_data: dict[str, Any],
    manager: DialogManager,
) -> None:
    manager.dialog_data.update(start_data)
    start_data.clear()


@aiogram_dialog_inject
async def getter(
    dialog_manager: DialogManager,
    *,
    localization: Localization,
    nft_gateway: NftDataGateway,
    currency_gateway: CurrencyExchangeRateDataGateway,
    **kwargs: Any,
) -> dict[str, Any]:
    dialog_data = dialog_manager.dialog_data
    nft = await nft_gateway.read(NftId(dialog_data["nft_id"]))
    crypto_currency_type = localization(
        f"currency-{nft.crypto_currency.value}",
    )
    crypto_exchange_rate = await currency_gateway.get_exchange_rate(
        from_currency=nft.currency,
        to_currency=nft.crypto_currency,
    )
    return {
        "media": MediaAttachment(
            type=ContentType.PHOTO,
            file_id=MediaId(nft.file_id),
        ),
        "localization": {
            "name": nft.name.name,
            "price": nft.price.price,
            "currency_type": nft.currency.value,
            "crypto_currency_type": crypto_currency_type,
            "crypto_price": crypto_exchange_rate.exchange(nft.price).price,
            "description": nft.description.description or LOCALIZATION_VOID,
        },
    }


@aiogram_dialog_inject
async def process_message(
    update: Message,
    _: MessageInput,
    manager: DialogManager,
    *,
    localization: Localization,
    interactor: UpdateNftInteractor,
) -> None:
    if update.text is None:
        await update.delete()
        manager.show_mode = ShowMode.NO_UPDATE
        return None

    try:
        data = NftDescription(update.text).description
    except NftDescriptionLengthError as error:
        await update.answer(
            localization(
                "nft-description-invalid-length",
                length=error.length,
            ),
        )
        return None

    await interactor(
        UpdateNftInDs(
            description=data,
            id=NftId(manager.dialog_data["nft_id"]),
        ),
    )
    manager.show_mode = ShowMode.DELETE_AND_SEND
    await update.delete()


dialog = Dialog(
    Window(
        LocalizationText("edit-nft-menu"),
        FixedDynamicMedia("media"),
        MessageInput(
            func=process_message,
            content_types=[ContentType.TEXT, ContentType.PHOTO],
        ),
        Cancel(
            LocalizationText("back"),
            show_mode=ShowMode.DELETE_AND_SEND,
        ),
        getter=getter,
        state=EditNftStates.main,
    ),
    on_start=on_start,
)
