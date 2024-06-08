from fastapi import APIRouter, Depends, HTTPException
from app.backend.auth import get_current_user
from app.models.models import User, UserInDB, Token
from app.backend.relations import *

routerRelation = APIRouter()

@routerRelation.post("/create_relation/")
def create_relation(relation: Relation, current_user: User = Depends(get_current_user)):
    try:
        relation.user1 = current_user.username
        if crear_relacion(relation):
            return {"status": "success", "message": "Relation created"}
        else:
            raise HTTPException(status_code=400, detail="Relation already exists")
            
    except:
        raise HTTPException(status_code=400, detail="Error creating relation")
    
@routerRelation.get("/relations/me/")
def read_relations_me(current_user: User = Depends(get_current_user)):
    try:
        relaciones = obtener_relaciones_por_username(current_user.username)
        if relaciones:
            return relaciones
        else:
            raise HTTPException(status_code=400, detail="No relations found")
    except:
        raise HTTPException(status_code=400, detail="Error reading relations")
    
@routerRelation.get("/relations/{username}/")
def read_relations(username: str, current_user: User = Depends(get_current_user)):
    try:
        relaciones = obtener_relaciones_por_username(username)
        if relaciones:
            return relaciones
        else:
            raise HTTPException(status_code=400, detail="No relations found")
    except:
        raise HTTPException(status_code=400, detail="Error reading relations")
    
@routerRelation.delete("/delete_relation/")
def delete_relation(relation: Relation, current_user: User = Depends(get_current_user)):
    try:
        relation.user1 = current_user.username
        if borrar_relacion(relation):
            return {"status": "success", "message": "Relation deleted"}
        else:
            raise HTTPException(status_code=400, detail="Error deleting relation")
    except:
        raise HTTPException(status_code=400, detail="Error deleting relation")
    
# @routerRelation.put("/update_relation/")
# def update_relation(relation: Relation, current_user: User = Depends(get_current_user)):
#     try:
#         relation.user1 = current_user.username
#         if borrar_relacion(relation):
#             if crear_relacion(relation):
#                 return {"status": "success", "message": "Relation updated"}
#             else:
#                 raise HTTPException(status_code=400, detail="Error updating relation")
#         else:
#             raise HTTPException(status_code=400, detail="Error updating relation")
#     except:
#         raise HTTPException(status_code=400, detail="Error updating relation")