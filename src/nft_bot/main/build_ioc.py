from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from dishka import AsyncContainer, make_async_container

from nft_bot.config import Config
from nft_bot.main.providers.config import ConfigProvider
from nft_bot.main.providers.connection import ConnectionProvider
from nft_bot.main.providers.context import ContextProvider
from nft_bot.main.providers.data_mappers import DataMappersProvider
from nft_bot.main.providers.id_providers import IdProvidersProvider
from nft_bot.main.providers.interactors import InteractorProvider
from nft_bot.main.providers.localization import LocalizationProvider
from nft_bot.main.providers.transaction_managers import (
    TransactionManagersProvider,
)
from nft_bot.presentation.localization import LocalizationStorage


@asynccontextmanager
async def build_ioc(
    config: Config,
    localization_storage: LocalizationStorage,
) -> AsyncIterator[AsyncContainer]:
    ioc = make_async_container(
        ConfigProvider(),
        ContextProvider(),
        ConnectionProvider(),
        DataMappersProvider(),
        InteractorProvider(),
        IdProvidersProvider(),
        LocalizationProvider(),
        TransactionManagersProvider(),
        context={
            Config: config,
            LocalizationStorage: localization_storage,
        },
    )
    try:
        yield ioc
    finally:
        await ioc.close()
