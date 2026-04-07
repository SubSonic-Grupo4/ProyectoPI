class ApplicationDTO:
    def __init__(self, idSolicitud, idProveedor, idEspacio, descripcion, categoriaServicio,
                 portfolioUrl=None, estado="PENDIENTE", fechaSolicitud=None):
        self.idSolicitud = idSolicitud
        self.idProveedor = idProveedor
        self.idEspacio = idEspacio
        self.descripcion = descripcion
        self.categoriaServicio = categoriaServicio
        self.portfolioUrl = portfolioUrl
        self.estado = estado
        self.fechaSolicitud = fechaSolicitud

    def to_dict(self):
        return {
            "idSolicitud": self.idSolicitud,
            "idProveedor": self.idProveedor,
            "idEspacio": self.idEspacio,
            "descripcion": self.descripcion,
            "categoriaServicio": self.categoriaServicio,
            "portfolioUrl": self.portfolioUrl,
            "estado": self.estado,
            "fechaSolicitud": self.fechaSolicitud
        }
