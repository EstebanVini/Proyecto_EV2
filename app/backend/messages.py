import datetime
import pytz
from app.database.databaseConn import databaseConn
from app.backend.users import obtener_usuario_por_username
from app.models.models import Relation, Message, User, MessageInDB


def enviar_mensaje(message: Message, current_user):
    conn, cursor = databaseConn()

    # obtener los datos del usuario actual
    usuario = obtener_usuario_por_username(current_user.username)

    # obtener la fecha y hora actual en hora local de la CDMX
    date = datetime.datetime.now(pytz.timezone('America/Mexico_City')).strftime("%Y-%m-%d %H:%M:%S")

    try:
        cursor.execute('INSERT INTO messages (userID, sender, receiver, message, date) VALUES (%s, %s, %s, %s, %s)',
                       (usuario.id, usuario.username , usuario.relatedto, message.message, date))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(e)
        return False
    
def obtener_mensajes_por_username(username: str):
    # crear la conexion con la base de datos
    conn, cursor = databaseConn()

    # ejecutar la consulta SQL para obtener los mensajes por username
    try:
        cursor.execute('SELECT * FROM messages WHERE sender = %s', (username,))
        mensajes = cursor.fetchall()
        # si se encontraron mensajes, retornarlos
        # cerrar la conexion con la base de datos
        conn.close()
        return [MessageInDB(id=mensaje[0], userID=mensaje[1], sender=mensaje[2], receiver=mensaje[3], message=mensaje[4], date=mensaje[5]) for mensaje in mensajes]
    except:
        return False
    
def obtener_mensajes_recibidos(username: str):
    # crear la conexion con la base de datos
    conn, cursor = databaseConn()

    # ejecutar la consulta SQL para obtener los mensajes por username
    try:
        cursor.execute('SELECT * FROM messages WHERE receiver = %s', (username,))
        mensajes = cursor.fetchall()
        # si se encontraron mensajes, retornarlos
        # cerrar la conexion con la base de datos
        conn.close()
        return [MessageInDB(id=mensaje[0], userID=mensaje[1], sender=mensaje[2], receiver=mensaje[3], message=mensaje[4], date=mensaje[5]) for mensaje in mensajes]
    except:
        return False
    
def obtener_mensajes_por_ID(userID: int):
    # crear la conexion con la base de datos
    conn, cursor = databaseConn()

    # ejecutar la consulta SQL para obtener los mensajes por username
    try:
        cursor.execute('SELECT * FROM messages WHERE userID = %s', (userID,))
        mensajes = cursor.fetchall()
        # si se encontraron mensajes, retornarlos
        # cerrar la conexion con la base de datos
        conn.close()
        return [MessageInDB(id=mensaje[0], userID=mensaje[1], sender=mensaje[2], receiver=mensaje[3], message=mensaje[4], date=mensaje[5]) for mensaje in mensajes]
    except:
        return False

def obtener_mensaje_recibido_aleatorio(username: str):
    # crear la conexion con la base de datos
    conn, cursor = databaseConn()

    # ejecutar la consulta SQL para obtener los mensajes por username
    try:
        cursor.execute('SELECT * FROM messages WHERE receiver = %s ORDER BY RAND() LIMIT 1', (username,))
        mensaje = cursor.fetchone()
        # si se encontraron mensajes, retornarlos
        # cerrar la conexion con la base de datos
        conn.close()
        return MessageInDB(id=mensaje[0], userID=mensaje[1], sender=mensaje[2], receiver=mensaje[3], message=mensaje[4], date=mensaje[5])
    except Exception as e:
        print(e)
        return False

def borrar_mensaje(id: int):
    # crear la conexion con la base de datos
    conn, cursor = databaseConn()

    # ejecutar la consulta SQL para borrar el mensaje
    try:
        cursor.execute('DELETE FROM messages WHERE id = %s', (id,))
        conn.commit()
        conn.close()
        return True
    except:
        return False
    
    


