import sqlite3
import time
import datetime
import json
import random
import bcrypt
from app.backend.databaseConn import badabaseConn

#____________________________________________Usuarios_______________________________________________________

def crear_BaseDatosusers():
    # crear una conexión a la base de datos
    conn, cursor = badabaseConn()

    # crear la tabla de usuarios con las columnas id, username, password y salt
    cursor.execute('CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT, salt TEXT)')

    # confirmar los cambios y cerrar la conexión a la base de datos
    conn.commit()
    conn.close()

def obtener_usuarios():
    # crear una conexión a la base de datos
    conn, cursor = badabaseConn()

    # ejecutar la consulta SQL para obtener todos los usuarios
    cursor.execute('SELECT * FROM users')

    # obtener todos los usuarios
    usuarios = cursor.fetchall()

    # cerrar la conexión a la base de datos
    conn.close()

    # retornar los usuarios
    return usuarios

def obtener_usuario_por_username(username: str):
    # crear una conexión a la base de datos
    conn, cursor = badabaseConn()

    # ejecutar la consulta SQL para obtener el usuario por username
    try:
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))

    except:
        return False

    usuario = cursor.fetchone()

    # cerrar la conexión a la base de datos
    conn.close()

    # si se encontró el usuario, retornar verdadero y si no se encontró, retornar falso
    if usuario:
        return {'id': usuario[0], 'username': usuario[1], 'password': usuario[2], 'salt': usuario[3]}
    
    else:
        return False

def hash_password(password, salt=None):
    pwd_bytes = password.encode("utf-8")
    if salt is None:
        salt = bcrypt.gensalt()
    else:
        salt = salt.encode("utf-8")
    hashed_pwd = bcrypt.hashpw(pwd_bytes, salt)
    return hashed_pwd.decode('utf-8'), salt.decode('utf-8')

def check_password(password, hashed_pwd, salt):
    salt = salt.encode("utf-8")
    pwd_bytes = password.encode("utf-8")
    return bcrypt.hashpw(pwd_bytes, salt) == hashed_pwd.encode("utf-8")

def crear_usuaio(data: dict):
    username = data['username']
    password = data['password']
    hasd_password, salt = hash_password(password)

    # crear una conexión a la base de datos
    conn, cursor = badabaseConn()

    # consultar si el usuario ya existe
    if obtener_usuario_por_username(username):
        return False
    
    # insertar un usuario en la tabla con un ID automático
    cursor.execute('INSERT INTO users (username, password, salt) VALUES (?, ?, ?)', (username, hasd_password, salt))

    # confirmar los cambios y cerrar la conexión a la base de datos
    conn.commit()
    conn.close()

    return True


def login(data: dict):
    username = data['username']
    password = data['password']

    # crear una conexión a la base de datos
    conn, cursor = badabaseConn()

    # consultar si el usuario ya existe
    usuario = obtener_usuario_por_username(username)

    # si el usuario no existe, retornar falso
    if not usuario:
        return False

    # si el usuario existe, verificar si la contraseña es correcta
    if check_password(password, usuario['password'], usuario['salt']):
        return True
    else:
        return False
    

def eliminar_usuario(username: str):

    # crear una conexión a la base de datos
    conn, cursor = badabaseConn()

    # consultar si el usuario ya existe
    usuario = obtener_usuario_por_username(username)

    # si el usuario no existe, retornar falso
    if not usuario:
        return False

    # si el usuario existe, eliminarlo de la base de datos
    cursor.execute('DELETE FROM users WHERE username = ?', (username,))

    # confirmar los cambios y cerrar la conexión a la base de datos
    conn.commit()
    conn.close()

    return True
