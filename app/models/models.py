# models.py
from pydantic import BaseModel
from typing import Optional


#_______________________________USER____________________________________
class User(BaseModel):
    username: str
    email: Optional[str] = None

class UserInDB(User):
    password: str
    salt: Optional[str] = None
    admin: Optional[bool] = False

#_______________________________TOKEN____________________________________

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None
