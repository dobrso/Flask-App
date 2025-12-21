from database.database import Database
from models.product import Product


class ProductRepository:
    def __init__(self):
        self.database = Database()

    def create(self, name, description, price, user_id, image=None):
        connection = self.database.getConnection()
        if connection:
            cursor = connection.cursor()
            query = '''
            INSERT INTO products (name, description, price, user_id, image)
            VALUES (%s, %s, %s, %s, %s)
            '''

            try:
                cursor.execute(query, (name, description, price, user_id, image))
                connection.commit()

            finally:
                cursor.close()
                connection.close()

    def getAll(self):
        connection = self.database.getConnection()
        if connection:
            cursor = connection.cursor()
            query = '''
            SELECT * FROM products
            '''

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

    def getById(self, id):
        connection = self.database.getConnection()
        if connection:
            cursor = connection.cursor()
            query = '''
            SELECT * FROM products
            WHERE id = %s
            '''

            try:
                cursor.execute(query, (id,))
                row = cursor.fetchone()
                if not row:
                    return None

            finally:
                cursor.close()
                connection.close()

            return Product(*row)

    def updateById(self, id, name, description, price, image=None):
        connection = self.database.getConnection()
        if connection:
            cursor = connection.cursor()

            try:
                if image:
                    query = '''
                    UPDATE products
                    SET name = %s, description = %s, price = %s, image = %s
                    WHERE id = %s
                    '''
                    cursor.execute(query, (name, description, price, image, id))

                else:
                    query = '''
                    UPDATE products
                    SET name = %s, description = %s, price = %s
                    WHERE id = %s
                    '''
                    cursor.execute(query, (name, description, price, id))

                connection.commit()

            finally:
                cursor.close()
                connection.close()

    def deleteById(self, id):
        connection = self.database.getConnection()
        if connection:
            cursor = connection.cursor()
            query = '''
            DELETE FROM products
            WHERE id = %s
            '''

            try:
                cursor.execute(query, (id,))
                connection.commit()

            finally:
                cursor.close()
                connection.close()

    def getProductOwner(self, id):
        connection = self.database.getConnection()
        if connection:
            cursor = connection.cursor()
            query = '''
            SELECT user_id
            FROM products
            WHERE id = %s
            '''

            try:
                cursor.execute(query, (id,))
                userID = cursor.fetchone()[0]
                if not userID:
                    return None

            finally:
                cursor.close()
                connection.close()

            return userID

    def getProductImage(self, id):
        connection = self.database.getConnection()
        if connection:
            cursor = connection.cursor()
            query = '''
            SELECT image
            FROM products
            WHERE id = %s
            '''

            try:
                cursor.execute(query, (id,))
                image = cursor.fetchone()[0]
                if not image:
                    return None

            finally:
                cursor.close()
                connection.close()

            return image
