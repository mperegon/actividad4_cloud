from pydantic import BaseModel
from typing import Optional

class UserBO(BaseModel):
    id: Optional[id] = None
    username: str
    passwort: str
    mail: str
    year_of_birth: int