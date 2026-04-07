class UserDTO:
    def __init__(self, id_usuario, rol, name, email, password, address, avatarUrl=None,
                 businessName=None, phone=None, biography="", socialLinks=None, gallery=None):
        self.id_usuario = id_usuario
        self.rol = rol
        self.name = name
        self.email = email
        self.password = password
        self.address = address
        self.avatarUrl = avatarUrl
        self.businessName = businessName
        self.phone = phone
        self.biography = biography or ""
        self.socialLinks = socialLinks or {
            "facebook": "",
            "instagram": "",
            "x": "",
            "website": ""
        }
        self.gallery = gallery or []

    def to_dict(self):
        return {
            "id_usuario": self.id_usuario,
            "rol": self.rol,
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "address": self.address,
            "avatarUrl": self.avatarUrl,
            "businessName": self.businessName,
            "phone": self.phone,
            "biography": self.biography,
            "socialLinks": self.socialLinks,
            "gallery": self.gallery
        }

    def to_public_dict(self):
        return {
            "id_usuario": self.id_usuario,
            "rol": self.rol,
            "name": self.name,
            "email": self.email,
            "address": self.address,
            "avatarUrl": self.avatarUrl,
            "businessName": self.businessName,
            "phone": self.phone,
            "biography": self.biography,
            "socialLinks": self.socialLinks,
            "gallery": self.gallery
        }
