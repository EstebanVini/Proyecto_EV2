import sqlite3

def badabaseConn():
    conn = sqlite3.connect('./data/proyectoE.db')
    cursor = conn.cursor()
    return conn, cursor