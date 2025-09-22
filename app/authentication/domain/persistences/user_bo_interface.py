from abc import ABC, abstractmethod
from app.authentication.domain.bo.user_bo import UserBO





class UserBOInterface(ABC):

    @abstractmethod

    async def create_user(self, user: UserBO):
        pass

    
    @abstractmethod
    async def get_user(self, username: str) -> UserBO:
        pass