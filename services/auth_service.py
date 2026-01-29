from utils.file_handler import FileHandler

USERS_FILE = "data/users.json"

class AuthService:
    def login(self, username, password):
        users = FileHandler.read(USERS_FILE)
        return any(u["username"] == username and u["password"] == password for u in users)
