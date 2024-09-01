import pymysql
from logger import logger

import os
from dotenv import load_dotenv
load_dotenv()

RELATION_DB_HOST = os.getenv("RELATION_DB_HOST", "localhost")
RELATION_DB_PORT = os.getenv("RELATION_DB_PORT", "3308")
RELATION_DB_USER = os.getenv("RELATION_DB_USER", "root")
RELATION_DB_PASSWD = os.getenv("RELATION_DB_PASSWD", "123456")
RELATION_DB_NAME = os.getenv("RELATION_DB_NAME", "douyin_crawler")


class Database:
    def __init__(self):
        params = {
            'host':RELATION_DB_HOST,
            'port':int(RELATION_DB_PORT),
            'user':RELATION_DB_USER,
            'password':RELATION_DB_PASSWD,
            'database':RELATION_DB_NAME,
            'charset':"utf8mb4",
            'cursorclass':pymysql.cursors.DictCursor,
        }

        logger.info('connectting database, params: ')
        print(params)
        self.connection = pymysql.connect(**params)

        logger.info('database version:')
        print(self.execute("select VERSION()"))
        
    def execute(self,sql):
        with self.connection.cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchall()
    
    def setup_table_schema():
        logger.error("plz setup table schema")


database = None
def get():
    global database
    if database is None:
        database = Database()
    return database
