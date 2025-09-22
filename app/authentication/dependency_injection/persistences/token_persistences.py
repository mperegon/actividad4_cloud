from dependency_injector import containers, providers

from app.authentication.persistence.memory.token import TokenMemoryPersistenceService



class TokenPersistences(containers.DeclarativeContainer):
    
    memory = providers.Singleton(
        TokenMemoryPersistenceService
    )

    carlemany = memory