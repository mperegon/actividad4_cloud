from abc import ABC, abstractmethod

class TokenInterface(ABC):
    @abstractmethod
    def generate_token(self,username:str) -> str:
        pass
    
    
    @abstractmethod
    def delete_token(self,token:str):
        pass

    
    
    @abstractmethod
    def get_username(self,username:str) -> str:
        pass