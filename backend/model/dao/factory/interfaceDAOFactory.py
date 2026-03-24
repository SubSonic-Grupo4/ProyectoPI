from abc import ABC, abstractmethod


class InterfaceDAOFactory(ABC):

    @abstractmethod
    def get_user_dao(self):
        pass

    @abstractmethod
    def get_ticket_dao(self):
        pass

    @abstractmethod
    def get_purchase_options_dao(self):
        pass
