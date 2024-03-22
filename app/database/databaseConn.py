# import sqlite3

# def badabaseConn():
#     conn = sqlite3.connect('./data/proyectoE.db')
#     cursor = conn.cursor()
#     return conn, cursor

import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv("dev.env")

# Datos de conexión
host = os.getenv("DBHOST")
user = os.getenv("DBUSER")
password = os.getenv("DBPASSWORD")
database = "proyectoEv2"


def badabaseConn():
    # Intenta establecer la conexión
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            charset='utf8mb4',  # Configura el conjunto de caracteres
            collation='utf8mb4_unicode_ci'  # Configura la colación
        )
        if connection.is_connected():
            print("Conexión establecida")
            return connection, connection.cursor()    

    except mysql.connector.Error as err:
        print("Error de conexión: {}".format(err))
        return None  
    
    return None
