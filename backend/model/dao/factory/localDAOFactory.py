from backend.model.dao.factory.interfaceDAOFactory import InterfaceDAOFactory
from backend.model.dao.local.localApplicationDAO import LocalApplicationDAO
from backend.model.dao.local.localPurchaseOptionsDAO import LocalPurchaseOptionsDAO
from backend.model.dao.local.localSpaceDAO import LocalSpaceDAO
from backend.model.dao.local.localStatsDAO import LocalStatsDAO
from backend.model.dao.local.localTicketDAO import LocalTicketDAO
from backend.model.dao.local.localUserDAO import LocalUserDAO


class LocalDAOFactory(InterfaceDAOFactory):

    def get_user_dao(self):
        return LocalUserDAO()

    def get_ticket_dao(self):
        return LocalTicketDAO()

    def get_purchase_options_dao(self):
        return LocalPurchaseOptionsDAO()

    def get_space_dao(self):
        return LocalSpaceDAO()

    def get_application_dao(self):
        return LocalApplicationDAO()

    def get_stats_dao(self):
        return LocalStatsDAO()
