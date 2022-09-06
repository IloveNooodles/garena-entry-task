import bcrypt

class HashPassword:
    def __init__(self, password):
        self.password = password.encode("latin-1")

    def hash(self):
        hashed_password = bcrypt.hashpw(self.password, bcrypt.gensalt())
        return hashed_password.decode("latin-1")

    def check(self, hashed_password):
        isMatched = bcrypt.checkpw(self.password, hashed_password.encode("latin-1"))
        return isMatched
