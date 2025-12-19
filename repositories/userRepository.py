from database.database import Database
from models.user import User


class UserRepository:
    def __init__(self):
        self.database = Database()

    def create(self, username, hashedPassword):
        connection = self.database.getConnection()
        if connection:
            cursor = connection.cursor()
            query = '''
                INSERT INTO users (username, password_hash)
                VALUES (%s, %s)
                RETURNING id
            '''

            try:
                cursor.execute(query, (username, hashedPassword))
                id = cursor.fetchone()[0]
                connection.commit()

            finally:
                cursor.close()
                connection.close()

            return self.getById(id)

    def getById(self, id):
        connection = self.database.getConnection()
        if connection:
            cursor = connection.cursor()
            query = '''
                SELECT * FROM users
                WHERE id = %s
            '''

            try:
                cursor.execute(query, (id,))
                row = cursor.fetchone()
                if not row:
                    return None

                connection.commit()

            finally:
                cursor.close()
                connection.close()

            return User(*row)

    def getByUsername(self, username):
        connection = self.database.getConnection()
        if connection:
            cursor = connection.cursor()
            query = '''
            SELECT * FROM users
            WHERE username = %s
            '''

            try:
                cursor.execute(query, (username,))
                row = cursor.fetchone()
                if not row:
                    return None

                connection.commit()

            finally:
                cursor.close()
                connection.close()

            return User(*row)
