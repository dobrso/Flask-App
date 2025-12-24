from database.database import Database
from models.profile import Profile


class ProfileRepository:
    def __init__(self):
        self.database = Database()

    def create(self, userId):
        connection = self.database.getConnection()
        if connection:
            cursor = connection.cursor()
            query = """
            INSERT INTO profiles (user_id)
            VALUES (%s)
            """

            try:
                cursor.execute(query, (userId,))
                connection.commit()

            finally:
                cursor.close()
                connection.close()

    def get(self, userId):
        connection = self.database.getConnection()
        if connection:
            cursor = connection.cursor()
            query = """
            SELECT * FROM profiles
            WHERE user_id = %s
            """

            try:
                cursor.execute(query, (userId,))
                row = cursor.fetchone()
                if not row:
                    return None

            finally:
                cursor.close()
                connection.close()

            return Profile(*row)

    def getId(self, userId):
        connection = self.database.getConnection()
        if connection:
            cursor = connection.cursor()
            query = """
            SELECT id
            FROM profiles
            WHERE user_id = %s
            """

            try:
                cursor.execute(query, (userId,))
                id = cursor.fetchone()
                if not id:
                    return None

            finally:
                cursor.close()
                connection.close()

            return id[0]

    def update(self, userId, bio, phoneNumber, image=None):
        connection = self.database.getConnection()
        if connection:
            cursor = connection.cursor()

            try:
                if image:
                    query = """
                    UPDATE profiles
                    SET bio = %s, phone_number = %s, image = %s
                    WHERE user_id = %s
                    """

                    cursor.execute(query, (bio, phoneNumber, image, userId))

                else:
                    query = """
                    UPDATE profiles
                    SET bio = %s, phone_number = %s
                    WHERE user_id = %s
                    """

                    cursor.execute(query, (bio, phoneNumber, userId))

                connection.commit()

            finally:
                cursor.close()
                connection.close()
