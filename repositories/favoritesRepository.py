from database.database import Database


class FavoritesRepository:
    def __init__(self):
        self.database = Database()

    def add(self, userId, productId):
        connection = self.database.getConnection()
        if connection:
            cursor = connection.cursor()
            query = """
            INSERT INTO favorites (user_id, product_id)
            VALUES (%s, %s)
            """

            try:
                cursor.execute(query, (userId, productId))
                connection.commit()

            finally:
                cursor.close()
                connection.close()

    def delete(self, userId, productId):
        connection = self.database.getConnection()
        if connection:
            cursor = connection.cursor()
            query = """
            DELETE FROM favorites
            WHERE user_id = %s AND product_id = %s
            """

            try:
                cursor.execute(query, (userId, productId))
                connection.commit()

            finally:
                cursor.close()
                connection.close()

    def getAll(self, userId):
        connection = self.database.getConnection()
        if connection:
            cursor = connection.cursor()
            query = """
            SELECT product_id
            FROM favorites
            WHERE user_id = %s
            """

            try:
                cursor.execute(query, (userId,))
                rows = cursor.fetchall()
                if not rows:
                    return None

            finally:
                cursor.close()
                connection.close()

            favorites = [row[0] for row in rows]
            return favorites
