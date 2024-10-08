import bcrypt
from app.database.databaseConn import databaseConn
from app.models.models import User, UserInDB, NewPassword

def obtener_usuario_por_username(username: str):
    # crear una conexión a la base de datos
    conn, cursor = databaseConn()

    # ejecutar la consulta SQL para obtener el usuario por username
    try:
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        usuario = cursor.fetchone()
        # si se encontró el usuario, retornar verdadero y si no se encontró, retornar falso
        # cerrar la conexión a la base de datos
        conn.close()
        user = UserInDB(id=usuario[0], username=usuario[1], email=usuario[2], password=usuario[3], salt=usuario[4], relatedto=usuario[5], admin=usuario[6])
        return user
    except:
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


def loginDB(user: UserInDB):
    # consultar si el usuario ya existe
    usuario = obtener_usuario_por_username(user.username)

    # si el usuario no existe, retornar falso
    if not usuario:
        return False

    # si el usuario existe, verificar si la contraseña es correcta
    if check_password(user.password, usuario.password, usuario.salt):
        return user
    else:
        return False
    
def register_userDB(user: UserInDB):

    hashed_pwd, salt = hash_password(user.password)

    # crear una conexión a la base de datos
    conn, cursor = databaseConn()

    # consultar si el usuario ya existe
    try:
        if obtener_usuario_por_username(user.username):
            return False
    except Exception as e:
        print(e)
        pass
        
    # insertar un usuario en la tabla con un ID automático
    try:
        # insertar un usuario en la tabla con un ID automático
        cursor.execute('INSERT INTO users (username, email, password, salt, admin) VALUES (%s, %s, %s, %s, %s)', (user.username, user.email, hashed_pwd, salt, False))
    except Exception as e:
        print(e)
        return False

    # confirmar los cambios y cerrar la conexión a la base de datos
    conn.commit()
    conn.close()

    return True

def chage_password_userDB(newPwd: NewPassword, user: UserInDB):
    # crear una conexión a la base de datos
    conn, cursor = databaseConn()

    # Consultar si el usuario ya existe y validar las credenciales
    try:
        if not loginDB(UserInDB(username=user.username, password=newPwd.password)):
            return False
    except Exception as e:
        print(e)
        return False
    
    # Actualizar la contraseña del usuario
    hashed_pwd, salt = hash_password(newPwd.newpassword)

    try:
        cursor.execute('UPDATE users SET password = %s, salt = %s WHERE username = %s', (hashed_pwd, salt, user.username))
    except Exception as e:
        print(e)
        return False
    finally:
        conn.commit()
        conn.close()

    return True
