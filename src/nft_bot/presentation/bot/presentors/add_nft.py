import operator
from decimal import Decimal
from typing import Any

from aiogram.enums import ContentType
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import Dialog, DialogManager, ShowMode, Window
from aiogram_dialog.api.entities import MediaAttachment, MediaId
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, Cancel, ManagedRadio, Radio
from aiogram_dialog.widgets.text import Const
from magic_filter import F

from nft_bot.application.currency_exchange_rate.data_gateway import \
    CurrencyExchangeRateDataGateway
from nft_bot.application.nft.interactors.create import (
    CreateNftInDs,
    CreateNftInteractor,
)
from nft_bot.consts import ZERO_DECIMAL
from nft_bot.domain.nft.entity import NftCryptoCurrencyType, NftCurrencyType
from nft_bot.domain.nft.errors import (
    NftDescriptionLengthError,
    NftNameLengthError,
    NftPriceError,
)
from nft_bot.domain.nft.value_objects import NftDescription, NftName, NftPrice
from nft_bot.main.injects import aiogram_dialog_inject
from nft_bot.presentation.bot.states import AddNftStates
from nft_bot.presentation.bot.utils import get_widget
from nft_bot.presentation.bot.widgets.media.dynamic_media import (
    FixedDynamicMedia,
)
from nft_bot.presentation.bot.widgets.text.localization import LocalizationText
from nft_bot.presentation.localization import (
    Localization,
    LOCALIZATION_NONE,
    LOCALIZATION_VOID,
)


VALUE_OBJECT_MAP: dict[str, tuple[Any, str]] = {
    "name": (NftName, "name"),
    "description": (NftDescription, "description"),
    "price": (lambda x: NftPrice(Decimal(x)), "price"),
}


@aiogram_dialog_inject
async def getter(
    dialog_manager: DialogManager,
    *,
    localization: Localization,
    currency_data_gateway: CurrencyExchangeRateDataGateway,
    **kwargs: Any,
) -> dict[str, Any]:
    dialog_data = dialog_manager.dialog_data
    
    currency_type_widget: ManagedRadio[NftCurrencyType]
    currency_type_widget = get_widget(
        widget_id="currency_type",
        dialog_manager=dialog_manager,
    )
    raw_currency_type = currency_type_widget.get_checked()
    if raw_currency_type:
        currency_type = raw_currency_type.value
    else:
        currency_type = None
    
    crypto_currency_type_widget: ManagedRadio[NftCryptoCurrencyType]
    crypto_currency_type_widget = get_widget(
        widget_id="crypto_currency_type",
        dialog_manager=dialog_manager,
    )
    raw_crypto_currency_type = crypto_currency_type_widget.get_checked()
    if raw_crypto_currency_type:
        crypto_currency_type = localization(
            f"currency-{raw_crypto_currency_type.value}",
        )
    else:
        crypto_currency_type = None
    
    price = dialog_data.get("price")
    name = dialog_data.get("name", LOCALIZATION_VOID)
    description = dialog_data.get("description", LOCALIZATION_VOID)
    
    file_id = dialog_data.get("file_id")
    if file_id:
        media = MediaAttachment(
            type=ContentType.PHOTO,
            file_id=MediaId(file_id),
        )
    else:
        media = None
    
    crypto_price: str | Decimal
    if price and raw_crypto_currency_type and raw_currency_type:
        crypto_exchange_rate = await currency_data_gateway.get_exchange_rate(
            from_currency=raw_currency_type,
            to_currency=raw_crypto_currency_type,
        )
        crypto_price = crypto_exchange_rate.exchange(
            NftPrice(Decimal(price))
        ).price
    else:
        crypto_price = LOCALIZATION_VOID
    
    ready_for_save = all(
        (
            name,
            price,
            file_id,
            currency_type,
            crypto_currency_type,
        ),
    )
    return {
        "media": media,
        "ready_for_save": ready_for_save,
        "localization": {
            "name": name,
            "description": description,
            "crypto_price": crypto_price,
            "price": Decimal(price) if price else ZERO_DECIMAL,
            "currency_type": currency_type or LOCALIZATION_NONE,
            "crypto_currency_type": crypto_currency_type or LOCALIZATION_VOID,
            "crypto_currency": (
                localization(f'currency-{raw_crypto_currency_type.value}')
                if raw_crypto_currency_type else LOCALIZATION_NONE
            ),
        },
    }


@aiogram_dialog_inject
async def process_message(
    update: Message,
    _: MessageInput,
    manager: DialogManager,
    *,
    localization: Localization,
) -> None:
    if update.text:
        widget: ManagedRadio[str] = get_widget(
            widget_id="enter_type",
            dialog_manager=manager,
        )
        checked = widget.get_checked()
        if checked is None:
            return None
        
        value_object, attr = VALUE_OBJECT_MAP[checked]
        try:
            data = getattr(value_object(update.text), attr)
        except NftNameLengthError as error:
            await update.answer(
                localization(
                    "nft-name-invalid-length",
                    length=error.length,
                ),
            )
            return None
        except NftDescriptionLengthError as error:
            await update.answer(
                localization(
                    "nft-description-invalid-length",
                    length=error.length,
                ),
            )
            return None
        except NftPriceError as error:
            await update.answer(
                localization("nft-price-invalid-length"),
            )
            return None
        except ArithmeticError:
            await update.answer(localization("nft-price-invalid-value"))
            return None
        
        manager.dialog_data[checked] = str(data)
        manager.show_mode = ShowMode.EDIT
        await update.delete()
    elif update.photo:
        manager.dialog_data["file_id"] = update.photo[-1].file_id
        manager.show_mode = ShowMode.EDIT
        await update.delete()
    else:
        manager.show_mode = ShowMode.NO_UPDATE
        await update.delete()


@aiogram_dialog_inject
async def save(
    update: CallbackQuery,
    widget: Button,
    manager: DialogManager,
    *,
    localization: Localization,
    interactor: CreateNftInteractor,
) -> None:
    dialog_data = manager.dialog_data
    currency_type = get_widget(
        widget_id="currency_type",
        dialog_manager=manager,
    ).get_checked()
    if currency_type is None:
        return None
    
    crypto_currency_type = get_widget(
        widget_id="crypto_currency_type",
        dialog_manager=manager,
    ).get_checked()
    if crypto_currency_type is None:
        return None
    
    await interactor(
        CreateNftInDs(
            name=dialog_data["name"],
            file_id=dialog_data["file_id"],
            price=Decimal(dialog_data["price"]),
            description=dialog_data.get("description"),
            currency=currency_type,
            crypto_currency=crypto_currency_type,
        ),
    )
    await update.answer(
        localization("nft-created"),
        show_alert=True,
    )
    await manager.done(show_mode=ShowMode.DELETE_AND_SEND)


dialog = Dialog(
    Window(
        LocalizationText("add-nft-menu"),
        FixedDynamicMedia("media"),
        MessageInput(
            func=process_message,
            content_types=[ContentType.TEXT, ContentType.PHOTO],
        ),
        Radio(
            Const("🔘") + LocalizationText("{item[0]}"),
            LocalizationText("{item[0]}"),
            id="enter_type",
            item_id_getter=operator.itemgetter(1),
            items=[
                ("name", "name"),
                ("price", "price"),
                ("description", "description"),
            ],
        ),
        Radio(
            Const("✔️") + LocalizationText("currency-{item}"),
            LocalizationText("currency-{item}"),
            id="currency_type",
            item_id_getter=lambda x: x,
            type_factory=NftCurrencyType,
            items=[_.value for _ in NftCurrencyType],
        ),
        Radio(
            Const("✔️") + LocalizationText("currency-{item}"),
            LocalizationText("currency-{item}"),
            id="crypto_currency_type",
            item_id_getter=lambda x: x,
            type_factory=NftCryptoCurrencyType,
            items=[_.value for _ in NftCryptoCurrencyType],
        ),
        Button(
            LocalizationText("save"),
            id="save",
            on_click=save,
            when=F["ready_for_save"],
        ),
        Cancel(
            LocalizationText("back"),
            show_mode=ShowMode.DELETE_AND_SEND,
        ),
        getter=getter,
        state=AddNftStates.main,
    ),
)
