from logging import getLogger
from typing import TYPE_CHECKING

from aiogram_dialog import setup_dialogs

from nft_bot.config import Config
from nft_bot.main.bot.setup import (
    create_dispatcher,
    create_fsm_sources,
    create_telegram_bot,
    set_commands,
    setup_handlers,
    setup_middleware,
)
from nft_bot.main.build_ioc import build_ioc
from nft_bot.presentation.bot.presentors.main import setup_routers
from nft_bot.presentation.localization import LocalizationStorage

if TYPE_CHECKING:
    from dishka import AsyncContainer

logger = getLogger(__name__)


async def run_bot(
    config: Config,
    localization_storage: LocalizationStorage,
) -> None:
    container: AsyncContainer
    async with build_ioc(
        config=config,
        localization_storage=localization_storage,
    ) as container:
        tg_bot_config = config.telegram_bot
        bot = create_telegram_bot(tg_bot_config.token)
        await set_commands(bot)

        fsm_sources = create_fsm_sources(tg_bot_config.storage_url)
        dispatcher = create_dispatcher(
            container=container,
            fsm_storage=fsm_sources[0],
            fsm_events_isolation=fsm_sources[1],
        )
        setup_routers(dispatcher)
        setup_handlers(dispatcher)
        setup_middleware(
            container=container,
            dispatcher=dispatcher,
        )

        dispatcher["bg_manager_factory"] = setup_dialogs(router=dispatcher)

        if tg_bot_config.skip_updates:
            await bot.delete_webhook(True)

        allowed_updates = dispatcher.resolve_used_update_types()
        logger.info(f"Allowed bot updates {allowed_updates!r}")

        await dispatcher.start_polling(
            bot,
            allowed_updates=allowed_updates,
        )
