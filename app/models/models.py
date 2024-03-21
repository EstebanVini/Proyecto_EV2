# models.py
from pydantic import BaseModel
from typing import Optional
from typing import List


#_______________________________USER____________________________________
class User(BaseModel):
    username: str

class UserInDB(User):
    password: str
    id: Optional[int] = None
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

#_______________________________MESSAGE____________________________________
class Message(BaseModel):
    message: str
    
class MessageInDB(Message):
    id: int
    userID: int
    sender: str
    receiver: str
    date: str

#_______________________________Movie____________________________________

class Movie(BaseModel):
    id: Optional[int] = None
    title: Optional[str] = None
    release: Optional[str] = None
    type: Optional[str] = None
    genre: Optional[str] = None
    imageurl: Optional[str] = None

class MovieInDB(Movie):
    user1: Optional[str] = None
    user2: Optional[str] = None


