from app.authentication.domain.persistences.token_persistences import TokenInterface
from app.authentication.domain.persistences.exceptions import TokenNotFound
import uuid

class TokenMemoryPersistenceService(TokenInterface):
  


    def __init__(self):
        self._token_db = {}

    def generate_token(self,username:str) -> str:
        random_id = sr(uuid.uuid4())
        while random_id in self._token_db:
            random_id= str(uuid.uuid4())
        self._token_db[random_id]=username
        return random_id
    
 
    def delete_token(self,token:str):
        if token not in self._token_db:
            raise TokenNotFound
        del self._token_db[token]

 
    def get_username(self,token:str) -> str:
        if token not in self._token_db:
            raise TokenNotFound
        del self._token_db[token]