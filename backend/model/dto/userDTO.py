class UserDTO:
    def __init__(self, id_usuario, rol, name, email, password, address, avatarUrl):
        self.id_usuario = id_usuario
        self.rol = rol
        self.name = name
        self.email = email
        self.password = password
        self.address = address
        self.avatarUrl = avatarUrl

    def to_dict(self):
        return {
            "id_usuario": self.id_usuario,
            "rol": self.rol,
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "address": self.address,
            "avatarUrl": self.avatarUrl
        }

    def to_public_dict(self):
        return {
            "id_usuario": self.id_usuario,
            "rol": self.rol,
            "name": self.name,
            "email": self.email,
            "address": self.address,
            "avatarUrl": self.avatarUrl
        }
