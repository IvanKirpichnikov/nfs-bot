from dishka import Provider, Scope, provide

from nft_bot.application.common.id_provider import IdProvider
from nft_bot.domain.profile.entity import ProfileId
from nft_bot.infrastructure.id_providers.profile_id import ProfileIdProvider


class IdProvidersProvider(Provider):
    scope = Scope.REQUEST

    provides = provide(
        ProfileIdProvider,
        provides=IdProvider[ProfileId],
    )
