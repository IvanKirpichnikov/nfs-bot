import logging
from argparse import ArgumentParser
from collections.abc import Callable, Coroutine
from enum import Enum
from pathlib import Path
from typing import Any, Protocol

from nft_bot.config import build_config
from nft_bot.main.bot.run import run_bot
from nft_bot.presentation.localization import build_localization_storage

asyncio_run: Callable[[Coroutine[Any, Any, Any]], None]
try:
    from uvloop import run as asyncio_run  # type: ignore[no-redef]
except ImportError:
    import asyncio

    asyncio_run = asyncio.run
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


class RunType(Enum):
    BOT = "bot"


class Arguments(Protocol):
    run: RunType | None
    config_path: Path | None


def run_application(
    arguments: Arguments,
    run_type: RunType,
) -> None:
    if run_type == RunType.BOT:
        if arguments.config_path is None:
            raise ValueError(arguments)

        logging.basicConfig(level=logging.DEBUG)
        config = build_config(path=arguments.config_path)
        localization_storage = build_localization_storage(config.localization)
        return asyncio_run(
            run_bot(
                config=config,
                localization_storage=localization_storage,
            ),
        )
    return None


def create_argument_parser() -> ArgumentParser:
    argparse = ArgumentParser(description="bijouterie application")
    run_app_group = argparse.add_argument_group(title="run application")
    run_app_group.add_argument(
        "--run",
        dest="run",
        type=RunType,
        required=False,
        default=None,
    )
    run_app_group.add_argument(
        "--config-path",
        dest="config_path",
        type=Path,
        required=False,
        default=None,
    )

    return argparse


def main() -> None:
    argument_parser = create_argument_parser()
    arguments: Arguments = argument_parser.parse_args()

    if arguments.run:
        run_application(arguments, arguments.run)
