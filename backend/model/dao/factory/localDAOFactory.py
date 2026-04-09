from backend.model.dao.factory.interfaceDAOFactory import InterfaceDAOFactory
from backend.model.dao.local.localPurchaseOptionsDAO import LocalPurchaseOptionsDAO
from backend.model.dao.local.localUserDAO import LocalUserDAO
from backend.model.dao.local.localTicketDAO import LocalTicketDAO


class LocalDAOFactory(InterfaceDAOFactory):

    def get_user_dao(self):
        return LocalUserDAO()

    def get_ticket_dao(self):
        return LocalTicketDAO()

    def get_purchase_options_dao(self):
        return LocalPurchaseOptionsDAO()
