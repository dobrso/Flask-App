class Product:
    def __init__(self, id, title, description, price, user_id, created_at, image=None):
        self.id = id
        self.title = title
        self.description = description
        self.price = price
        self.user_id = user_id
        self.creation_at = created_at
        self.image = image
