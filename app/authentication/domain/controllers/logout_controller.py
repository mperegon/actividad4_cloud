from app.authentication.domain.persistences.token_persstences import TokenInterface


class LogoutController:
        def __init__(self, token_persistence_service: TokenInterface):
        
        self._token_persistence_service = token_persistence_service

    async def __init__(self,token: str):
        self._token_persistence_service.delete_token(token=token)