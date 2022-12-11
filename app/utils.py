import psycopg2
from psycopg2.extras import RealDictCursor
from passlib.context import CryptContext
import time
from .config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    return pwd_context.hash(password)

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def connectDb():
    over = False
    while not over:
        try:
            conn = psycopg2.connect(host = settings.database_hostname, database = settings.database_name,
            user = settings.database_username, 
            password = settings.database_password, cursor_factory=RealDictCursor)
            cursor = conn.cursor()
            print('Database connection was succesfull')
            over = True
        except Exception as error:
            time.sleep(2)
            print('Failed: ', error)
    return conn, cursor