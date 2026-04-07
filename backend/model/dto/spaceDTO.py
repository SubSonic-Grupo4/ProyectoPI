class SpaceDTO:
    def __init__(self, idEspacio, tipo, tamano, precio, disponible, descripcion, ubicacion):
        self.idEspacio = idEspacio
        self.tipo = tipo
        self.tamano = tamano
        self.precio = precio
        self.disponible = disponible
        self.descripcion = descripcion
        self.ubicacion = ubicacion

    def to_dict(self):
        return {
            "idEspacio": self.idEspacio,
            "tipo": self.tipo,
            "tamano": self.tamano,
            "precio": self.precio,
            "disponible": self.disponible,
            "descripcion": self.descripcion,
            "ubicacion": self.ubicacion
        }
