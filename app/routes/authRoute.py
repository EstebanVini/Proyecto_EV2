# routers.py
from fastapi import APIRouter, Depends, HTTPException
from app.backend.auth import create_access_token, get_current_user
from app.backend.users import register_userDB, loginDB, chage_password_userDB
from app.models.models import User, UserInDB, Token, NewPassword

routerAuth = APIRouter()

@routerAuth.post("/register/")
def register_user(user: UserInDB):
    try:
        if register_userDB(user):
            return {"status": "success", "message": "User created"}
        else:
            raise HTTPException(status_code=400, detail="User already exists")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=f"Error creating user: {e}")    
    
@routerAuth.post("/token/", response_model=Token)
def login(user: UserInDB):
    try:
        user = loginDB(user)
        if not user:
            raise HTTPException(status_code=401, detail="Incorrect username or password")
        access_token = create_access_token(data={"sub": user.username})
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error logging in: {e}")

# ruta para cambiar la contraseña de un usuario
@routerAuth.put("/users/change_password/")
def change_password(newPass: NewPassword, current_user: User = Depends(get_current_user)):
    try:
        if chage_password_userDB(newPass, current_user):
            return {"status": "success", "message": "Password changed"}
        else:
            raise HTTPException(status_code=400, detail="Error changing password")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="Error changing password")


@routerAuth.get("/users/me/", response_model=User)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
