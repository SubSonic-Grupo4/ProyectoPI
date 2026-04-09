from backend.model.dao.local.localConnector import LocalConnector
from backend.model.dto.userDTO import UserDTO


class LocalUserDAO:
    def __init__(self):
        self.connector = LocalConnector()
        self.filename = "users.json"

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

    def update_provider_profile(self, id_usuario, name, email, address, avatarUrl=None,
                                businessName=None, phone=None, biography=None, socialLinks=None):
        users = self.connector.read_json(self.filename)
        for user in users:
            if user["id_usuario"] == id_usuario:
                user["name"] = name
                user["email"] = email
                user["address"] = address
                user["avatarUrl"] = avatarUrl
                user["businessName"] = businessName
                user["phone"] = phone
                user["biography"] = biography or ""
                user["socialLinks"] = socialLinks or {
                    "facebook": "",
                    "instagram": "",
                    "x": "",
                    "website": ""
                }
                self.connector.write_json(self.filename, users)
                return UserDTO(**user)
        return None

    def add_gallery_image(self, id_usuario, image_url):
        users = self.connector.read_json(self.filename)
        for user in users:
            if user["id_usuario"] == id_usuario:
                gallery = user.get("gallery", [])
                gallery.append(image_url)
                user["gallery"] = gallery
                self.connector.write_json(self.filename, users)
                return UserDTO(**user)
        return None
