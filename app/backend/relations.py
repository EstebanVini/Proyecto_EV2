from app.database.databaseConn import badabaseConn
from app.models.models import Relation
from app.backend.users import obtener_usuario_por_username
from fastapi import HTTPException

def obtener_relaciones_por_username(username: str):
    # crear una conexión a la base de datos
    conn, cursor = badabaseConn()

    # ejecutar la consulta SQL para obtener el usuario por username
    try:
        cursor.execute('SELECT * FROM relations WHERE user1 = ? OR user2 = ?', (username, username))

    except:
        return False

    relaciones = cursor.fetchall()

    # cerrar la conexión a la base de datos
    conn.close()

    # si se encontró el usuario, retornar verdadero y si no se encontró, retornar falso
    if relaciones:
        return [Relation(id=relacion[0], user1=relacion[1], user2=relacion[2]) for relacion in relaciones]
    
    else:
        return False
    
def crear_relacion(relation: Relation):
    if relation.user1 == relation.user2:
        return False
    # crear una conexión a la base de datos
    conn, cursor = badabaseConn()

    # Verificar si los usuarios existen
    if not obtener_usuario_por_username(relation.user1) or not obtener_usuario_por_username(relation.user2):
        return False
    
    # verificar si la relación ya existe en ese orden o en el orden inverso
    try:
        cursor.execute('SELECT * FROM relations WHERE user1 = ? AND user2 = ?', (relation.user1, relation.user2))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="Relation already exists")
        cursor.execute('SELECT * FROM relations WHERE user1 = ? AND user2 = ?', (relation.user2, relation.user1))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="Relation already exists")
    except:
        return False
    
    # ejecutar la consulta SQL para crear la relación
    try:
        cursor.execute('INSERT INTO relations (user1, user2) VALUES (?, ?)', (relation.user1, relation.user2))
        conn.commit()
    except:
        return False
    
    # cerrar la conexión a la base de datos
    conn.close()
    return True

def borrar_relacion(relation: Relation):
    # crear una conexión a la base de datos
    conn, cursor = badabaseConn()

    # ejecutar la consulta SQL para borrar la relación
    try:
        cursor.execute('DELETE FROM relations WHERE user1 = ? AND user2 = ?', (relation.user1, relation.user2))
        conn.commit()
    except:
        return False
    
    # cerrar la conexión a la base de datos
    conn.close()
    return True