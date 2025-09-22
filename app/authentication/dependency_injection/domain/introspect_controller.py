from dependency_injector import containers, providers

from app.authentication.dependency_injection.persistences.token_persistences import TokenPersistences
from app.authentication.dependency_injection.persistences.user_bo_persistences import UserBOPersistences
from app.authentication.domain.controllers.introspect_controller import IntrospectController



class IntrospectControllers(containers.DeclarativeContainer):
    
    v1 = providers.Singleton(
        IntrospectController,
        user_bo_persistence_service = UserBOPersistences.carlemany(),
        token_persistence_service = TokenPersistences.carlemany(),
    )

    carlemany = v1