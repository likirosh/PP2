from config import DB_NAME, USER, PASSWORD, HOST, PORT
import psycopg2
conn = psycopg2.connect(
    dbname=DB_NAME,
    user=USER,
    password=PASSWORD,
    host=HOST,
    port=PORT
)
cur = conn.cursor()
print("Connected successfully")