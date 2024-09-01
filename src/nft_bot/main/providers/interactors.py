from dishka import Provider, Scope, provide

from nft_bot.application.common.id_provider import IdProvider
from nft_bot.application.currency_exchange_rate.data_gateway import (
    CurrencyExchangeRateDataGateway,
)
from nft_bot.application.nft.data_gateway import NftDataGateway
from nft_bot.application.nft.interactors.create import CreateNftInteractor
from nft_bot.application.nft.interactors.update import UpdateNftInteractor
from nft_bot.application.profile.data_gateway import ProfileDataGateway
from nft_bot.application.profile.interactors.create import (
    CreateProfileInteractor,
)
from nft_bot.application.profile.interactors.read import (
    ReadProfileDataInteractor,
)
from nft_bot.application.profile.interactors.update import (
    UpdateProfileInteractor,
)
from nft_bot.domain.profile.entity import ProfileId
from nft_bot.infrastructure.transaction_managers.database import (
    DatabaseTransactionManager,
)


class InteractorProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def create_nft(
        self,
        data_gateway: NftDataGateway,
        profile_id_provider: IdProvider[ProfileId],
        gateway_transaction_manager: DatabaseTransactionManager,
    ) -> CreateNftInteractor:
        return CreateNftInteractor(
            data_gateway=data_gateway,
            profile_id_provider=profile_id_provider,
            gateway_transaction_manager=gateway_transaction_manager,
        )

    @provide
    def update_nft(
        self,
        data_gateway: NftDataGateway,
        gateway_transaction_manager: DatabaseTransactionManager,
    ) -> UpdateNftInteractor:
        return UpdateNftInteractor(
            data_gateway=data_gateway,
            gateway_transaction_manager=gateway_transaction_manager,
        )

    @provide
    def create_profile(
        self,
        data_gateway: ProfileDataGateway,
        profile_id_provider: IdProvider[ProfileId],
        gateway_transaction_manager: DatabaseTransactionManager,
    ) -> CreateProfileInteractor:
        return CreateProfileInteractor(
            data_gateway=data_gateway,
            gateway_transaction_manager=gateway_transaction_manager,
        )

    @provide
    def update_profile(
        self,
        data_gateway: ProfileDataGateway,
        profile_id_provider: IdProvider[ProfileId],
        gateway_transaction_manager: DatabaseTransactionManager,
    ) -> UpdateProfileInteractor:
        return UpdateProfileInteractor(
            data_gateway=data_gateway,
            profile_id_provider=profile_id_provider,
            gateway_transaction_manager=gateway_transaction_manager,
        )

    @provide
    def read_profile_data(
        self,
        nft_data_gateway: NftDataGateway,
        profile_data_gateway: ProfileDataGateway,
        currency_data_gateway: CurrencyExchangeRateDataGateway,
    ) -> ReadProfileDataInteractor:
        return ReadProfileDataInteractor(
            nft_data_gateway=nft_data_gateway,
            profile_data_gateway=profile_data_gateway,
            currency_data_gateway=currency_data_gateway,
        )
