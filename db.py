import os
from dotenv import load_dotenv

load_dotenv()

DB_CLUSTER = os.getenv('DB_CLUSTER')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_COLLECTION = os.getenv('DB_COLLECTION')


def get_db_conn_str():
    return f'mongodb+srv://{DB_USER}:{DB_PASS}@{DB_CLUSTER}.sjaxqcy.mongodb.net/{DB_NAME}?retryWrites=true&w=majority'
