import psycopg2
import os
from dotenv import load_dotenv

load_dotenv("dev.env")

# Datos de conexión
host = "192.168.100.123"
user = os.getenv("DBUSER")
password = os.getenv("DBPASSWORD")
database = "ProyectoEV2"


def databaseConn():
    # Intenta establecer la conexión
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            dbname=database,
            #options="-c search_path=public"  # Opcionalmente puedes configurar el esquema
        )
        print("Conexión establecida")
        return connection, connection.cursor()

    except psycopg2.Error as err:
        print("Error de conexión: {}".format(err))
        return None