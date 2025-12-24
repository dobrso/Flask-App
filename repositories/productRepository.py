from database.database import Database
from models.product import Product


class ProductRepository:
    def __init__(self):
        self.database = Database()

    def create(self, title, description, price, user_id, image=None):
        connection = self.database.getConnection()
        if connection:
            cursor = connection.cursor()
            query = """
            INSERT INTO products (title, description, price, user_id, image)
            VALUES (%s, %s, %s, %s, %s)
            """

            try:
                cursor.execute(query, (title, description, price, user_id, image))
                connection.commit()

            finally:
                cursor.close()
                connection.close()

    def getAll(self):
        connection = self.database.getConnection()
        if connection:
            cursor = connection.cursor()
            query = """
            SELECT * FROM products
            """

            try:
                cursor.execute(query)
                rows = cursor.fetchall()
                if not rows:
                    return None

            finally:
                cursor.close()
                connection.close()

            products = [Product(*row) for row in rows]
            return products

    def get(self, id):
        connection = self.database.getConnection()
        if connection:
            cursor = connection.cursor()
            query = """
            SELECT * FROM products
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

            return Product(*row)

    def update(self, id, title, description, price, image=None):
        connection = self.database.getConnection()
        if connection:
            cursor = connection.cursor()

            try:
                if image:
                    query = """
                    UPDATE products
                    SET title = %s, description = %s, price = %s, image = %s
                    WHERE id = %s
                    """

                    cursor.execute(query, (title, description, price, image, id))

                else:
                    query = """
                    UPDATE products
                    SET title = %s, description = %s, price = %s
                    WHERE id = %s
                    """

                    cursor.execute(query, (title, description, price, id))

                connection.commit()

            finally:
                cursor.close()
                connection.close()

    def delete(self, id):
        connection = self.database.getConnection()
        if connection:
            cursor = connection.cursor()
            query = """
            DELETE FROM products
            WHERE id = %s
            """

            try:
                cursor.execute(query, (id,))
                connection.commit()

            finally:
                cursor.close()
                connection.close()

    def getOwner(self, id):
        connection = self.database.getConnection()
        if connection:
            cursor = connection.cursor()
            query = """
            SELECT user_id
            FROM products
            WHERE id = %s
            """

            try:
                cursor.execute(query, (id,))
                userId = cursor.fetchone()[0]
                if not userId:
                    return None

            finally:
                cursor.close()
                connection.close()

            return userId

    def getImage(self, id):
        connection = self.database.getConnection()
        if connection:
            cursor = connection.cursor()
            query = """
            SELECT image
            FROM products
            WHERE id = %s
            """

            try:
                cursor.execute(query, (id,))
                image = cursor.fetchone()[0]
                if not image:
                    return None

            finally:
                cursor.close()
                connection.close()

            return image
