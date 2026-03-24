from backend.model.dao.factory.localDAOFactory import LocalDAOFactory


class Model:
    def __init__(self):
        self.factory = LocalDAOFactory()
        self.user_dao = self.factory.get_user_dao()
        self.ticket_dao = self.factory.get_ticket_dao()
        self.purchase_options_dao = self.factory.get_purchase_options_dao()

    def login(self, email, password):
        user = self.user_dao.get_user_by_email(email)
        if user and user.password == password:
            return user
        return None

    def get_user_profile(self, id_usuario):
        return self.user_dao.get_user_by_id(id_usuario)

    def update_user_profile(self, id_usuario, name, email, address, avatarUrl=None):
        return self.user_dao.update_user_profile(
            id_usuario=id_usuario,
            name=name,
            email=email,
            address=address,
            avatarUrl=avatarUrl
        )

    def get_tickets_by_user(self, id_usuario):
        return self.ticket_dao.get_tickets_by_user(id_usuario)

    def get_ticket_by_id(self, ticket_id):
        return self.ticket_dao.get_ticket_by_id(ticket_id)

    def cancel_ticket(self, ticket_id):
        return self.ticket_dao.cancel_ticket(ticket_id)

    def purchase_tickets(self, id_usuario, eventName, dateLabel, passType, quantity):
        user = self.user_dao.get_user_by_id(id_usuario)
        if not user or quantity < 1:
            return None

        return self.ticket_dao.purchase_tickets(
            id_usuario=id_usuario,
            eventName=eventName,
            dateLabel=dateLabel,
            passType=passType,
            quantity=quantity
        )

    def get_purchase_options(self):
        return self.purchase_options_dao.get_purchase_options()
