from app.authentication.domain.persistences.token_persstences import TokenInterface
from app.authentication.domain.persistences.user_bo_interface import UserBOInterface




class IntrospectController:
    def __init__(self, user_bo_persistence_service: UserBOInterface, token_persistence_service: TokenInterface):
        self._user_bo_persistence_service = user_bo_persistence_service
        self._token_persistence_service = token_persistence_service

    async def __init__(self, token: str):
        username = self._token_persistence_service.get_username(token=token)
        return await self._user_bo_persistence_service(username=username)