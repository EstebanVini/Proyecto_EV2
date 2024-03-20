# routers.py
from fastapi import APIRouter, Depends, HTTPException
from app.backend.auth import create_access_token, get_current_user
from app.backend.users import register_userDB, loginDB
from app.models.models import User, UserInDB, Token

routerAuth = APIRouter()

@routerAuth.post("/register/")
def register_user(user: UserInDB):
    try:
        if register_userDB(user):
            return {"status": "success", "message": "User created"}
        else:
            raise HTTPException(status_code=400, detail="User already exists")
    except:
        raise HTTPException(status_code=400, detail="User already exists")    
    
@routerAuth.post("/token/", response_model=Token)
def login(user: UserInDB):
    user = loginDB(user)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@routerAuth.get("/users/me/", response_model=User)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
