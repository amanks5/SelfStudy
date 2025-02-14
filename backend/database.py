from urllib.parse import urlparse
import psycopg2
import os

connection_url = urlparse(os.getenv("POSTGRES_CONNECTION"))

connection = psycopg2.connect(
    database = connection_url.path[1:],
    user = connection_url.username,
    password = connection_url.password,
    host = connection_url.hostname,
    port = connection_url.port
)

def getCurrentDatabase():
    cursor = connection.cursor()
    cursor.execute("SELECT current_database();")
    result = cursor.fetchone()
    if result is None:
        return None
    return result[0]
