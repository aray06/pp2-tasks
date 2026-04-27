import psycopg2
import os

# Параметры подключения
params = {
    "host": "localhost",
    "database": "phonebook_db",
    "user": "postgres",
    "password": "qazxcvfdt", 
    "port": "5433"
}

def get_connection():
    conn = psycopg2.connect(**params)
    conn.set_client_encoding('UTF8')
    return conn