class User:
    def __init__(self, id, name, password_hash, created_at):
        self.id = id
        self.name = name
        self.password_hash = password_hash
        self.created_at = created_at
