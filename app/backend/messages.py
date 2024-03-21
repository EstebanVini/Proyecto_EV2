import datetime
import pytz
from app.database.databaseConn import badabaseConn
from app.backend.users import obtener_usuario_por_username
from app.models.models import Relation, Message, User, MessageInDB


def enviar_mensaje(message: Message, current_user: User):

    # crear la conexion con la base de datos
    conn, cursor = badabaseConn()

    # obtener datos del usuario
    try:
        sender = obtener_usuario_por_username(current_user.username)
        id_sender = sender.id
        reciever = sender.relatedto
        # obtener fecha y hora actual en hora local de la CDMX
        date = datetime.datetime.now(pytz.timezone('America/Mexico_City'))
        # dar formato a la fecha y hora en hora local de la CDMX
        date = date.strftime("%Y-%m-%d %H:%M:%S")
  
        if reciever is None:
            return False
    except:
        return False
    
    # ejecutar la consulta SQL para enviar el mensaje
    try:
        cursor.execute('INSERT INTO messages (userID, sender, receiver, message, date) VALUES (?, ?, ?, ?, datetime("now"))', (id_sender, current_user.username, reciever, message.message))
        conn.commit()
        conn.close()
        return True
    except:
        return False
    
def obtener_mensajes_por_username(username: str):
    # crear la conexion con la base de datos
    conn, cursor = badabaseConn()

    # ejecutar la consulta SQL para obtener los mensajes por username
    try:
        cursor.execute('SELECT * FROM messages WHERE sender = ?', (username,))
        mensajes = cursor.fetchall()
        # si se encontraron mensajes, retornarlos
        # cerrar la conexion con la base de datos
        conn.close()
        return [MessageInDB(id=mensaje[0], userID=mensaje[1], sender=mensaje[2], receiver=mensaje[3], message=mensaje[4], date=mensaje[5]) for mensaje in mensajes]
    except:
        return False
    
def obtener_mensajes_recibidos(username: str):
    # crear la conexion con la base de datos
    conn, cursor = badabaseConn()

    # ejecutar la consulta SQL para obtener los mensajes por username
    try:
        cursor.execute('SELECT * FROM messages WHERE receiver = ?', (username,))
        mensajes = cursor.fetchall()
        # si se encontraron mensajes, retornarlos
        # cerrar la conexion con la base de datos
        conn.close()
        return [MessageInDB(id=mensaje[0], userID=mensaje[1], sender=mensaje[2], receiver=mensaje[3], message=mensaje[4], date=mensaje[5]) for mensaje in mensajes]
    except:
        return False
    
def obtener_mensajes_por_ID(userID: int):
    # crear la conexion con la base de datos
    conn, cursor = badabaseConn()

    # ejecutar la consulta SQL para obtener los mensajes por username
    try:
        cursor.execute('SELECT * FROM messages WHERE userID = ?', (userID,))
        mensajes = cursor.fetchall()
        # si se encontraron mensajes, retornarlos
        # cerrar la conexion con la base de datos
        conn.close()
        return [MessageInDB(id=mensaje[0], userID=mensaje[1], sender=mensaje[2], receiver=mensaje[3], message=mensaje[4], date=mensaje[5]) for mensaje in mensajes]
    except:
        return False
    
def borrar_mensaje(id: int):
    # crear la conexion con la base de datos
    conn, cursor = badabaseConn()

    # ejecutar la consulta SQL para borrar el mensaje
    try:
        cursor.execute('DELETE FROM messages WHERE id = ?', (id,))
        conn.commit()
        conn.close()
        return True
    except:
        return False
    
    


