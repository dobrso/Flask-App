from database.database import Database
from models.profile import Profile


class ProfileRepository:
    def __init__(self):
        self.database = Database()

    def create(self, userID):
        connection = self.database.getConnection()
        if connection:
            cursor = connection.cursor()
            query = '''
            INSERT INTO profiles (user_id)
            VALUES (%s)
            '''

            try:
                cursor.execute(query, (userID,))
                connection.commit()

            finally:
                cursor.close()
                connection.close()

    def getProfile(self, userID):
        connection = self.database.getConnection()
        if connection:
            cursor = connection.cursor()
            query = '''
            SELECT * FROM profiles
            WHERE user_id = %s
            '''

            try:
                cursor.execute(query, (userID,))
                row = cursor.fetchone()
                if not row:
                    return None

            finally:
                cursor.close()
                connection.close()

            return Profile(*row)