from database.database import Database
from models.user import User


class UserRepository:
    def __init__(self):
        self.database = Database()

    def create(self, name, passwordHash):
        connection = self.database.getConnection()
        if connection:
            cursor = connection.cursor()
            query = """
                INSERT INTO users (name, password_hash)
                VALUES (%s, %s)
                RETURNING id
            """

            try:
                cursor.execute(query, (name, passwordHash))
                id = cursor.fetchone()
                connection.commit()

            finally:
                cursor.close()
                connection.close()

            return self.getById(id[0])

    def getById(self, id):
        connection = self.database.getConnection()
        if connection:
            cursor = connection.cursor()
            query = """
                SELECT * FROM users
                WHERE id = %s
            """

            try:
                cursor.execute(query, (id,))
                row = cursor.fetchone()
                if not row:
                    return None

            finally:
                cursor.close()
                connection.close()

            return User(*row)

    def getByName(self, name):
        connection = self.database.getConnection()
        if connection:
            cursor = connection.cursor()
            query = """
            SELECT * FROM users
            WHERE name = %s
            """

            try:
                cursor.execute(query, (name,))
                row = cursor.fetchone()
                if not row:
                    return None

            finally:
                cursor.close()
                connection.close()

            return User(*row)
