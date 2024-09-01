from collections.abc import Callable, Container
from inspect import Parameter
from typing import Any, Final, cast

from dishka import DEFAULT_COMPONENT, AsyncContainer, DependencyKey
from dishka.integrations.base import default_parse_dependency, wrap_injection

CONTAINER_KEY: Final[str] = "dishka_container"


def kw_only_parse_dependency(
    parameter: Parameter,
    hint: Any,
) -> DependencyKey | None:
    res = default_parse_dependency(parameter, hint)
    if res:
        return res
    elif parameter.kind == Parameter.KEYWORD_ONLY:
        return DependencyKey(hint, DEFAULT_COMPONENT)
    return None


def aiogd_container_getter(
    args: tuple[Any, ...],
    kwargs: dict[str, Any],
) -> AsyncContainer:
    if not args:
        container = kwargs[CONTAINER_KEY]
    elif len(args) == 2:
        container = args[-1].middleware_data[CONTAINER_KEY]
    else:
        container = args[2].middleware_data[CONTAINER_KEY]
    return cast(AsyncContainer, container)


def aiogram_dialog_inject[T](func: Callable[..., T]) -> Callable[..., T]:
    return wrap_injection(
        func=func,
        is_async=True,
        container_getter=aiogd_container_getter,
        parse_dependency=kw_only_parse_dependency,
    )


def aiogram_handler_inject[**P, T](func: Callable[P, T]) -> Callable[P, T]:
    additional_params = [
        Parameter(
            name=CONTAINER_KEY,
            annotation=Container,
            kind=Parameter.KEYWORD_ONLY,
        ),
    ]

    return wrap_injection(
        func=func,
        is_async=True,
        additional_params=additional_params,
        parse_dependency=kw_only_parse_dependency,
        container_getter=lambda _, p: p[CONTAINER_KEY],
    )
