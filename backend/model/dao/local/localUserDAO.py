from backend.model.dao.local.localConnector import LocalConnector
from backend.model.dto.userDTO import UserDTO


class LocalUserDAO:
    def __init__(self):
        self.connector = LocalConnector()
        self.filename = "users.json"

    def get_all_users(self):
        data = self.connector.read_json(self.filename)
        return [UserDTO(**user) for user in data]

    def get_user_by_email(self, email):
        users = self.connector.read_json(self.filename)
        for user in users:
            if user["email"] == email:
                return UserDTO(**user)
        return None

    def get_user_by_id(self, id_usuario):
        users = self.connector.read_json(self.filename)
        for user in users:
            if user["id_usuario"] == id_usuario:
                return UserDTO(**user)
        return None

    def update_user_profile(self, id_usuario, name, email, address, avatarUrl=None):
        users = self.connector.read_json(self.filename)

        for user in users:
            if user["id_usuario"] == id_usuario:
                user["name"] = name
                user["email"] = email
                user["address"] = address

                if avatarUrl is not None:
                    user["avatarUrl"] = avatarUrl

                self.connector.write_json(self.filename, users)
                return UserDTO(**user)

        return None
