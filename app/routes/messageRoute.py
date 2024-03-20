from fastapi import APIRouter, Depends, HTTPException
from app.backend.auth import get_current_user
from app.models.models import User, Message
from app.backend.messages import enviar_mensaje, obtener_mensajes_por_username, obtener_mensajes_recibidos, borrar_mensaje

routerMessage = APIRouter()

@routerMessage.post("/send_message/")
def send_message(message: Message, current_user: User = Depends(get_current_user)):
    try:
        if enviar_mensaje(message, current_user):
            return {"status": "success", "message": "Message sent"}
        else:
            raise HTTPException(status_code=400, detail="Error sending message")
    except:
        raise HTTPException(status_code=400, detail="Error sending message")
    
@routerMessage.get("/messages/me/")
def read_messages_me(current_user: User = Depends(get_current_user)):
    try:
        mensajes = obtener_mensajes_por_username(current_user.username)
        if mensajes:
            return mensajes
        else:
            raise HTTPException(status_code=400, detail="No messages found")
    except:
        raise HTTPException(status_code=400, detail="Error reading messages")
    
@routerMessage.get("/messages/{username}/")
def read_messages(username: str, current_user: User = Depends(get_current_user)):
    try:
        mensajes = obtener_mensajes_por_username(username)
        if mensajes:
            return mensajes
        else:
            raise HTTPException(status_code=400, detail="No messages found")
    except:
        raise HTTPException(status_code=400, detail="Error reading messages")
    
@routerMessage.get("/messages/recieved/")
def read_messages_recieved(current_user: User = Depends(get_current_user)):
    try:
        mensajes = obtener_mensajes_recibidos(current_user)
        if mensajes:
            return mensajes
        else:
            raise HTTPException(status_code=400, detail="No messages found")
    except:
        raise HTTPException(status_code=400, detail="Error reading messages")
    
@routerMessage.delete("/delete_message/{id}/")
def delete_message(id: int, current_user: User = Depends(get_current_user)):
    try:
        if borrar_mensaje(id):
            return {"status": "success", "message": "Message deleted"}
        else:
            raise HTTPException(status_code=400, detail="Error deleting message")
    except:
        raise HTTPException(status_code=400, detail="Error deleting message")

