import operator
from typing import TYPE_CHECKING, Any, Final

from aiogram import F
from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, DialogManager, ShowMode, Window
from aiogram_dialog.widgets.kbd import (
    Cancel,
    Column,
    CurrentPage,
    FirstPage,
    LastPage,
    NextPage,
    PrevPage,
    Row,
    Select,
    StubScroll,
)
from aiogram_dialog.widgets.text import Format

from nft_bot.application.common.id_provider import IdProvider
from nft_bot.application.nft.data_gateway import NftDataGateway
from nft_bot.application.nft.data_structure import (
    NftPaginateFromProfileGatewayDs,
)
from nft_bot.domain.profile.entity import ProfileId
from nft_bot.main.injects import aiogram_dialog_inject
from nft_bot.presentation.bot.states import EditNftStates, PaginationNftStates
from nft_bot.presentation.bot.utils import calculate_number_pages, get_widget
from nft_bot.presentation.bot.widgets.text.localization import LocalizationText

if TYPE_CHECKING:
    from aiogram_dialog.widgets.common.scroll import ManagedScroll

LIMIT: Final = 10


@aiogram_dialog_inject
async def getter(
    dialog_manager: DialogManager,
    *,
    gateway: NftDataGateway,
    profile_id_provider: IdProvider[ProfileId],
    **kwargs: Any,
) -> dict[str, Any]:
    scroll_widget: ManagedScroll = get_widget(
        dialog_manager=dialog_manager,
        widget_id="scroll",
    )
    page = await scroll_widget.get_page()
    profile_id = await profile_id_provider()
    nfts = await gateway.paginate_from_profile(
        NftPaginateFromProfileGatewayDs(
            limit=LIMIT,
            offset=page * LIMIT,
            profile_id=profile_id,
        ),
    )
    return {
        "nfts": nfts,
        "pages": calculate_number_pages(
            limit=LIMIT,
            total_count=await gateway.read_total_count(profile_id),
        ),
    }


async def nft_process(
    update: CallbackQuery,
    widget: Select[int],
    manager: DialogManager,
    data: int,
) -> None:
    await manager.start(
        data={"nft_id": data},
        state=EditNftStates.main,
        show_mode=ShowMode.DELETE_AND_SEND,
    )


dialog = Dialog(
    Window(
        LocalizationText("pagination-nft"),
        StubScroll(
            id="scroll",
            pages="pages",
        ),
        Column(
            Select(
                Format("{item.name.name}"),
                id="nfts",
                items="nfts",
                type_factory=int,
                on_click=nft_process,
                item_id_getter=operator.attrgetter("id"),
            ),
        ),
        Row(
            FirstPage(
                id="first_page",
                scroll="scroll",
                when=F["pages"] > 3,
            ),
            PrevPage(
                id="prev_page",
                scroll="scroll",
            ),
            CurrentPage(
                id="current_page",
                scroll="scroll",
                text=Format("{current_page1}/{pages}"),
            ),
            NextPage(
                id="next_page",
                scroll="scroll",
            ),
            LastPage(
                id="last_page",
                scroll="scroll",
                when=F["pages"] > 3,
            ),
            when=F["pages"] > 1,
        ),
        Cancel(
            LocalizationText("back"),
            show_mode=ShowMode.DELETE_AND_SEND,
        ),
        getter=getter,
        state=PaginationNftStates.main,
    ),
)
