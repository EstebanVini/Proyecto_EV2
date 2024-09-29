from app.database.databaseConn import databaseConn
from app.models.models import Relation
from app.backend.users import obtener_usuario_por_username
from fastapi import HTTPException

def crear_relacion(relation: Relation):
    # crear una conexión a la base de datos
    conn, cursor = databaseConn()

    # revisar si el usuario 2 existe
    try:
        cursor.execute('SELECT * FROM users WHERE username = %s', (relation.user2,))
        usuario = cursor.fetchone()
        if not usuario:
            raise HTTPException(status_code=400, detail="User 2 does not exist")
    except:
        return False
    
    # revisar si la relación ya existe
    try:
        cursor.execute('SELECT * FROM users WHERE relatedto = %s or relatedto = %s', (relation.user1, relation.user2))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="Relation already exists")
    except:
        return False
    
    # ejecutar la consulta SQL para crear la relación
    try:
        # ejecutar la consulta SQL para crear la relación
        cursor.execute('UPDATE users SET relatedto = %s WHERE username = %s', (relation.user2, relation.user1))
        cursor.execute('UPDATE users SET relatedto = %s WHERE username = %s', (relation.user1, relation.user2))
        conn.commit()
        conn.close()
        return True
    except:
        return False
    
def obtener_relaciones_por_username(username: str):
    # crear una conexión a la base de datos
    conn, cursor = databaseConn()

    # ejecutar la consulta SQL para obtener las relaciones por username
    try:
        cursor.execute('SELECT * FROM users WHERE username = %s and relatedto is not null', (username,))
        relaciones = cursor.fetchall()
        # si se encontraron relaciones, retornarlas
        # cerrar la conexión a la base de datos
        conn.close()
        return Relation(user1=relaciones[0][1], user2=relaciones[0][5])
    except:
        return False
    
def borrar_relacion(relation: Relation):
    # crear una conexión a la base de datos
    conn, cursor = databaseConn()

    # ejecutar la consulta SQL para borrar la relación
    try:
        cursor.execute('UPDATE users SET relatedto = NULL WHERE username = %s and relatedto = %s', (relation.user1, relation.user2))
        cursor.execute('UPDATE users SET relatedto = NULL WHERE username = %s and relatedto = %s', (relation.user2, relation.user1))
        conn.commit()
        conn.close()
        return True
    except:
        return False
    
    
