class StatsDTO:
    def __init__(self, totalSolicitudes, solicitudesPendientes, solicitudesAprobadas,
                 solicitudesRechazadas, profileViews, totalVentas, monthlyReservations,
                 activityLog):
        self.totalSolicitudes = totalSolicitudes
        self.solicitudesPendientes = solicitudesPendientes
        self.solicitudesAprobadas = solicitudesAprobadas
        self.solicitudesRechazadas = solicitudesRechazadas
        self.profileViews = profileViews
        self.totalVentas = totalVentas
        self.monthlyReservations = monthlyReservations
        self.activityLog = activityLog

    def to_dict(self):
        return {
            "totalSolicitudes": self.totalSolicitudes,
            "solicitudesPendientes": self.solicitudesPendientes,
            "solicitudesAprobadas": self.solicitudesAprobadas,
            "solicitudesRechazadas": self.solicitudesRechazadas,
            "profileViews": self.profileViews,
            "totalVentas": self.totalVentas,
            "monthlyReservations": self.monthlyReservations,
            "activityLog": self.activityLog
        }
