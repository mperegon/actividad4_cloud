from dependency_injector import containers, providers

from app.authentication.dependency_injection.persistences.user_bo_persistences import UserBOPersistences
from app.authentication.domain.controllers.register_controller import RegisterController



class RegisterControllers(containers.DeclarativeContainer):
    
    v1 = providers.Singleton(
        RegistreCrontroller,
        user_bo_persistence_service = UserBOPersistences.carlemany(),
    )

    carlemany = v1