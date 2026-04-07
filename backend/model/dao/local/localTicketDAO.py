from backend.model.dao.local.localConnector import LocalConnector
from backend.model.dto.ticketDTO import TicketDTO
from datetime import datetime


class LocalTicketDAO:
    def __init__(self):
        self.connector = LocalConnector()
        self.filename = "tickets.json"

    def get_all_tickets(self):
        data = self.connector.read_json(self.filename)
        return [TicketDTO(**ticket) for ticket in data]

    def get_tickets_by_user(self, id_usuario):
        tickets = self.connector.read_json(self.filename)
        return [
            TicketDTO(**ticket)
            for ticket in tickets
            if ticket["id_usuario"] == id_usuario and ticket.get("status") != "Cancelada"
        ]

    def get_ticket_by_id(self, ticket_id):
        tickets = self.connector.read_json(self.filename)
        for ticket in tickets:
            if ticket["ticketId"] == ticket_id:
                return TicketDTO(**ticket)
        return None

    def cancel_ticket(self, ticket_id):
        tickets = self.connector.read_json(self.filename)
        updated = False

        for ticket in tickets:
            if ticket["ticketId"] == ticket_id:
                ticket["status"] = "Cancelada"
                updated = True
                break

        if updated:
            self.connector.write_json(self.filename, tickets)

        return updated

    def purchase_tickets(self, id_usuario, eventName, dateLabel, passType, quantity):
        tickets = self.connector.read_json(self.filename)
        created_tickets = []

        next_number = self._get_next_ticket_number(tickets)
        month_day = self._build_month_day(dateLabel)

        for _ in range(quantity):
            ticket_data = {
                "ticketId": f"T-{next_number}",
                "eventName": eventName,
                "dateLabel": dateLabel,
                "monthDay": month_day,
                "passType": passType,
                "status": "Activa",
                "id_usuario": id_usuario
            }

            tickets.append(ticket_data)
            created_tickets.append(TicketDTO(**ticket_data))
            next_number += 1

        self.connector.write_json(self.filename, tickets)
        return created_tickets

    def _get_next_ticket_number(self, tickets):
        max_number = 1000

        for ticket in tickets:
            ticket_id = ticket.get("ticketId", "")
            if ticket_id.startswith("T-"):
                try:
                    number = int(ticket_id.split("-")[1])
                    if number > max_number:
                        max_number = number
                except ValueError:
                    continue

        return max_number + 1

    def _build_month_day(self, dateLabel):
        try:
            parsed_date = datetime.strptime(dateLabel, "%d/%m/%Y")
            return parsed_date.strftime("%b %d").upper()
        except ValueError:
            return dateLabel
