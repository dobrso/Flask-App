from database.database import Database


class FavoritesRepository:
    def __init__(self):
        self.database = Database()

    def add(self, userID, productID):
        connection = self.database.getConnection()
        if connection:
            cursor = connection.cursor()
            query = """
            INSERT INTO favorites (user_id, product_id)
            VALUES (%s, %s)
            """

            try:
                cursor.execute(query, (userID, productID))
                connection.commit()

            finally:
                cursor.close()
                connection.close()

    def delete(self, userID, productID):
        connection = self.database.getConnection()
        if connection:
            cursor = connection.cursor()
            query = """
            DELETE FROM favorites
            WHERE user_id = %s AND product_id = %s
            """

            try:
                cursor.execute(query, (userID, productID))
                connection.commit()

            finally:
                cursor.close()
                connection.close()

    def getAll(self, userID):
        connection = self.database.getConnection()
        if connection:
            cursor = connection.cursor()
            query = '''
            SELECT product_id
            FROM favorites
            WHERE user_id = %s
            '''

            try:
                cursor.execute(query, (userID,))
                result = cursor.fetchall()
                if not result:
                    return None

            finally:
                cursor.close()
                connection.close()

            favorites = [item[0] for item in result]
            return favorites
