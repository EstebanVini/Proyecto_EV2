# models.py
from pydantic import BaseModel
from typing import Optional


#_______________________________USER____________________________________
class User(BaseModel):
    username: str

class UserInDB(User):
    password: str
    email: Optional[str] = None
    salt: Optional[str] = None
    relatedto: Optional[str] = None
    admin: Optional[bool] = False

#_______________________________TOKEN____________________________________

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

#_______________________________RELATION____________________________________
class Relation(BaseModel):
    user1: Optional[str] = None
    user2: str
