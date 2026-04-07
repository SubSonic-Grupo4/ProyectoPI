from backend.model.dao.local.localConnector import LocalConnector
from backend.model.dto.statsDTO import StatsDTO


class LocalStatsDAO:
    def __init__(self):
        self.connector = LocalConnector()
        self.filename = "providerStats.json"

    def get_stats_by_provider(self, id_proveedor, pending, approved, rejected):
        stats = self.connector.read_json(self.filename)
        for entry in stats:
            if entry["idProveedor"] == id_proveedor:
                dto = StatsDTO(
                    totalSolicitudes=pending + approved + rejected,
                    solicitudesPendientes=pending,
                    solicitudesAprobadas=approved,
                    solicitudesRechazadas=rejected,
                    profileViews=entry["profileViews"],
                    totalVentas=entry["totalVentas"],
                    monthlyReservations=entry["monthlyReservations"],
                    activityLog=entry["activityLog"],
                )
                return dto
        return StatsDTO(
            totalSolicitudes=pending + approved + rejected,
            solicitudesPendientes=pending,
            solicitudesAprobadas=approved,
            solicitudesRechazadas=rejected,
            profileViews=0,
            totalVentas=0,
            monthlyReservations=[],
            activityLog=[],
        )
