from app.authentication.domain.bo.user_bo import UserBO
from app.authentication.domain.persistences.user_bo_interface import UserBOInterface
from app.authentication.domain.persistences.exceptions import UsernameAlreadyTakenException



class UserMemoryPersistenceService(UserBOInterface):

    def __init__(self):
        self_user_db = {}


    async def create_user(self, user: UserBO):
        if user.username in self._user_db:
            raise UsernameAlreadyTakenException()
        self._user_db[user.username] = user
        return user.username

    

    async def get_user(self, username: str) -> UserBO:
        if username not in self._user_db:
            raise UserNotFoundException()
        return self._user_db[username]