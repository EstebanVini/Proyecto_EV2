import bcrypt
from app.database.databaseConn import badabaseConn
from app.models.models import User, UserInDB

#____________________________________________Usuarios_______________________________________________________

def obtener_usuario_por_username(username: str):
    # crear una conexión a la base de datos
    conn, cursor = badabaseConn()

    # ejecutar la consulta SQL para obtener el usuario por username
    try:
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        usuario = cursor.fetchone()
        # si se encontró el usuario, retornar verdadero y si no se encontró, retornar falso
        # cerrar la conexión a la base de datos
        conn.close()
        user = UserInDB(username=usuario[1], email=usuario[2], password=usuario[3], salt=usuario[4], admin=usuario[5])
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
    conn, cursor = badabaseConn()

    # consultar si el usuario ya existe
    try:
        if obtener_usuario_por_username(user.username):
            return False
    except:
        pass
        
    # insertar un usuario en la tabla con un ID automático
    try:
        # insertar un usuario en la tabla con un ID automático
        cursor.execute('INSERT INTO users (username, email, password, salt, admin) VALUES (?, ?, ?, ?, ?)', (user.username, user.email, hashed_pwd, salt, 0))
    except:
        return False

    # confirmar los cambios y cerrar la conexión a la base de datos
    conn.commit()
    conn.close()

    return True
