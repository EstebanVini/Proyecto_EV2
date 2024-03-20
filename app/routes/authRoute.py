# routers.py
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.backend.auth import *
from app.backend.users import register_userDB, loginDB
from app.database.databaseConn import badabaseConn
from app.models.models import User, UserInDB, Token

routerAuth = APIRouter()

@routerAuth.post("/register/")
def register_user(user: UserInDB):
    try:
        register_userDB(user)
        return {"status": "success", "message": "User created"}
    except:
        raise HTTPException(status_code=400, detail="Error creating user")    
    

@routerAuth.post("/token/", response_model=Token)
def login(user: UserInDB):
    user = loginDB(user)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# @routerAuth.post("/logout/")
# def logout(request: Request, current_user: User = Depends(get_current_user)):
#     token = request.headers.get('Authorization')
#     if token:
#         revoked_tokens.add(token)
#     return JSONResponse(content={"message": "Logout successful"})

@routerAuth.get("/users/me/", response_model=User)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
