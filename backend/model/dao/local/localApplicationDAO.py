from datetime import datetime

from backend.model.dao.local.localConnector import LocalConnector
from backend.model.dto.applicationDTO import ApplicationDTO


class LocalApplicationDAO:
    def __init__(self):
        self.connector = LocalConnector()
        self.filename = "applications.json"

    def get_applications_by_provider(self, id_proveedor):
        applications = self.connector.read_json(self.filename)
        provider_apps = []
        for application in applications:
            if application["idProveedor"] == id_proveedor:
                provider_apps.append(ApplicationDTO(**application))
        return provider_apps

    def create_application(self, id_proveedor, id_espacio, descripcion, categoria_servicio, portfolio_url=None):
        applications = self.connector.read_json(self.filename)
        next_id = f"S-{len(applications) + 1:03d}"
        record = {
            "idSolicitud": next_id,
            "idProveedor": id_proveedor,
            "idEspacio": id_espacio,
            "descripcion": descripcion,
            "categoriaServicio": categoria_servicio,
            "portfolioUrl": portfolio_url,
            "estado": "PENDIENTE",
            "fechaSolicitud": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        }
        applications.append(record)
        self.connector.write_json(self.filename, applications)
        return ApplicationDTO(**record)

    def count_by_state(self, id_proveedor, estado):
        applications = self.connector.read_json(self.filename)
        return len([
            application for application in applications
            if application["idProveedor"] == id_proveedor and application["estado"] == estado
        ])

    def has_open_request_for_space(self, id_proveedor, id_espacio):
        applications = self.connector.read_json(self.filename)
        for application in applications:
            if (
                application["idProveedor"] == id_proveedor and
                application["idEspacio"] == id_espacio and
                application["estado"] in ("PENDIENTE", "APROBADA")
            ):
                return True
        return False
