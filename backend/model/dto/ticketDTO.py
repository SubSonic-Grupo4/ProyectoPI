class TicketDTO:
    def __init__(self, ticketId, eventName, dateLabel, monthDay, passType, status, id_usuario):
        self.ticketId = ticketId
        self.eventName = eventName
        self.dateLabel = dateLabel
        self.monthDay = monthDay
        self.passType = passType
        self.status = status
        self.id_usuario = id_usuario

    def to_dict(self):
        return {
            "ticketId": self.ticketId,
            "eventName": self.eventName,
            "dateLabel": self.dateLabel,
            "monthDay": self.monthDay,
            "passType": self.passType,
            "status": self.status,
            "id_usuario": self.id_usuario
        }