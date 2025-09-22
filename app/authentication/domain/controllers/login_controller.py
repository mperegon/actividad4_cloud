from app.authentication.domain.persistences.token_persstences import TokenInterface
from app.authentication.domain.persistences.user_bo_interface import UserBOInterface
from hashlib import sha256

class LoginController:
      def __init__(self, user_bo_persistence_service: UserBOInterface, token_persistence_service: TokenInterface):
        
        self._user_bo_persistence_service = user_bo_persistence_service
        self._token_persistence_service = token_persistence_service

    async def __init__(self,username: str, password: str) -> str:
        stored_user = await self._user_bo_persistence_service.get_user(username=username)
        hashed_stored_password = stored_user.password
        hash_password = username + password
        hashed_input_password = sha256 (hash_password.encode()).hexdigest()
        if hashed_stored_password == hashed_input_password:
            token = self._token_persistence_service.generate_token(username=username)
            return token
        else:
            raise WrongPasswordException()