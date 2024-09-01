from aiogram import Dispatcher

from . import add_nft, edit_nft, pagintation_nft, profile, settings


def setup_routers(dispatcher: Dispatcher) -> None:
    include_router = dispatcher.include_router
    include_router(profile.dialog)
    include_router(add_nft.dialog)
    include_router(settings.dialog)
    include_router(pagintation_nft.dialog)
    include_router(edit_nft.dialog)
