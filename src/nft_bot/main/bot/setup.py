from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart, ExceptionTypeFilter, or_f
from aiogram.fsm.storage.base import (
    BaseEventIsolation,
    BaseStorage,
    DefaultKeyBuilder,
)
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import BotCommand, ErrorEvent
from aiogram_dialog import DialogManager, ShowMode, StartMode
from aiogram_dialog.api.exceptions import UnknownIntent, UnknownState
from dishka import AsyncContainer
from dishka.integrations.aiogram import AutoInjectMiddleware
from redis.asyncio import Redis

from nft_bot.presentation.bot.middlewares.container import ContainerMiddleware
from nft_bot.presentation.bot.presentors.profile import start_profile
from nft_bot.presentation.bot.states import ProfileStates


async def restart_dialog(
    event: ErrorEvent,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.start(
        mode=StartMode.RESET_STACK,
        state=ProfileStates.main,
        show_mode=ShowMode.DELETE_AND_SEND,
    )


async def set_commands(bot: Bot) -> None:
    await bot.set_my_commands(
        commands=[
            BotCommand(
                command="/start",
                description="Старт/перезагрузка бота",
            ),
            BotCommand(
                command="/profile",
                description="Профиль",
            ),
        ],
    )


def create_telegram_bot(token: str) -> Bot:
    return Bot(
        token=token,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML,
        ),
    )


def create_fsm_sources(url: str) -> tuple[BaseStorage, BaseEventIsolation]:
    storage = RedisStorage(
        redis=Redis.from_url(url=url),
        key_builder=DefaultKeyBuilder(
            with_bot_id=True,
            with_destiny=True,
        ),
    )
    event_isolation = storage.create_isolation()
    return storage, event_isolation


def setup_middleware(
    *,
    dispatcher: Dispatcher,
    container: AsyncContainer,
) -> None:
    container_ = ContainerMiddleware(container)
    autoinject = AutoInjectMiddleware()

    for update in dispatcher.resolve_used_update_types():
        if update != "update":
            dispatcher.observers[update].middleware(autoinject)

    dispatcher.update.outer_middleware(container_)


def setup_handlers(dispatcher: Dispatcher) -> None:
    dispatcher.errors.register(
        restart_dialog,
        ExceptionTypeFilter(
            UnknownIntent,
            UnknownState,
        ),
    )
    dispatcher.message.register(
        start_profile,
        or_f(
            CommandStart(),
            Command("profile"),
        ),
    )


def create_dispatcher(
    container: AsyncContainer,
    fsm_storage: BaseStorage,
    fsm_events_isolation: BaseEventIsolation,
) -> Dispatcher:
    return Dispatcher(
        name=__name__,
        storage=fsm_storage,
        events_isolation=fsm_events_isolation,
    )
