from typing import Any, Final, cast, override

from adaptix import Retort, loader
from psycopg import AsyncConnection

from nft_bot.application.profile.data_gateway import ProfileDataGateway
from nft_bot.application.profile.data_structure import (
    CreateProfileGatewayDs,
    UpdateProfileGatewayDs,
)
from nft_bot.application.profile.errors import NotFoundProfileError
from nft_bot.domain.profile.entity import (
    Profile,
    TgUserId,
)
from nft_bot.domain.profile.value_objects import ProfileName

retort = Retort(
    recipe=[
        loader(ProfileName, ProfileName),
    ],
)

CREATE_QUERY = """
    INSERT INTO profile(
        name,
        tg_user_id,
        tg_chat_id,
        currency_type
    )
    VALUES (%s, %s, %s, %s);
"""
READ_QUERY: Final = """
    SELECT
        id,
        name,
        tg_user_id,
        tg_chat_id,
        currency_type
    FROM profile
    WHERE tg_user_id = %s;
"""
EXISTS_QUERY: Final = """
    SELECT EXISTS(
        SELECT id
        FROM profile
        WHERE tg_user_id = %s
    );
"""
UPDATE_QUERY: Final = """
    UPDATE profile
    SET
        name = COALESCE(%s, name),
        currency_type = COALESCE(%s, currency_type)
    WHERE id = %s;
"""


class ProfileDataMapper(ProfileDataGateway):
    def __init__(
        self,
        connection: AsyncConnection[Any],
    ) -> None:
        self._connection = connection

    @override
    async def create(self, data: CreateProfileGatewayDs) -> None:
        await self._connection.execute(
            query=CREATE_QUERY,
            params=(
                data.name,
                data.tg_user_id,
                data.tg_chat_id,
                data.currency_type.value,
            ),
        )

    @override
    async def read(self, data: TgUserId) -> Profile:
        cursor = await self._connection.execute(
            query=READ_QUERY,
            params=(data,),
        )
        fetchone = await cursor.fetchone()
        if fetchone is None:
            raise NotFoundProfileError("By tg user id %r" % data)
        return retort.load(fetchone, Profile)

    @override
    async def exists(self, data: TgUserId) -> bool:
        cursor = await self._connection.execute(
            query=EXISTS_QUERY,
            params=(data,),
        )
        fetchone = await cursor.fetchone()
        if fetchone is None:
            raise NotFoundProfileError("By tg user id %r" % data)
        return cast(bool, fetchone["exists"])

    @override
    async def update(self, data: UpdateProfileGatewayDs) -> None:
        await self._connection.execute(
            query=UPDATE_QUERY,
            params=(
                data.name,
                data.currency_type.value if data.currency_type else None,
                data.id,
            ),
        )
