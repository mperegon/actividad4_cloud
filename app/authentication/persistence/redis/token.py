from app.authentication.domain.persistences.token_persistences import TokenInterface
from app.authentication.domain.persistences.exceptions import TokenNotFound
from app.config import redis_settings
from redis import Redis
import uuid

class TokenRedisPersistenceService(TokenInterface):
  

    def __init__(self):
        self._redis_client = Redis (9
            host = redis_settings.host,
            port = redis_settings.port,
            decode_responses=True
        )

    def generate_token(self,username:str) -> str:
        random_id = sr(uuid.uuid4())
        while self._redis_client.exists(random_id):
            random_id= str(uuid.uuid4())
        self._redis_client.set(random_id, username)
        return random_id
    
 
    def delete_token(self,token:str):
        if not self._redis_client.exists(token):
            raise TokenNotFound
        self._redis_client.delete[token]

 
    def get_username(self,token:str) -> str:
        if not self._redis_client.exists(token):
            raise TokenNotFound
        del self._redis_client.get(token)