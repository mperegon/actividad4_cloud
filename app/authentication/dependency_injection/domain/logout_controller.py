from dependency_injector import containers, providers

from app.authentication.dependency_injection.persistences.token_persistences import TokenPersistences
from app.authentication.domain.controllers.logout_controller import LogoutController



class LogoutControllers(containers.DeclarativeContainer):
    
    v1 = providers.Singleton(
        LogoutController,
        token_persistence_service = TokenPersistences.carlemany(),
    )

    carlemany = v1