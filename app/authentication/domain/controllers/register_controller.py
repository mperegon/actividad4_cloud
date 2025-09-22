from app.authentication.domain.persistences.user_bo_interface import UserBOInterface
from app.authentication.domain.bo.user_bo import UserBO
from hashlib import sha256


class RegisterController:
    def __init__(self, user_bo_persistence_service: UserBOInterface):
        
        self._user_bo_persistence_service = user_bo_persistence_service

    async def __init__(self,username: str, password: str, mail: str, year_of_birth: int) -> UserBO:
        hash_password = username + password
        hashed_input_password = sha256 (hash_password.encode()).hexdigest()
        new_user = UserBO(
            username=username, 
            passsword=hashed_input_password,
            mail=mail
            year_of_birth=year_of_birth,
        )
        await self._user_bo_persistence_service.create_user(new_user)

        return new_user