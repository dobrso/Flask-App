import os

import psycopg2

from config import Config


class Database:
    def getConnection(self):
        connection = psycopg2.connect(
            dbname=Config.DB_NAME,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            host=Config.DB_HOST,
            port=Config.DB_PORT
        )
        return connection

    def initDB(self):
        connection = self.getConnection()

        currentDir = os.path.dirname(os.path.abspath(__file__))
        initFile = os.path.join(currentDir, 'initDB.sql')

        with open(initFile, "r", encoding="utf-8") as file:
            query = file.read()

        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()

        cursor.close()
        connection.close()
