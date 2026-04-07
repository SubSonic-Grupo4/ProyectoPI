from abc import ABC, abstractmethod


class InterfaceDAOFactory(ABC):

    @abstractmethod
    def get_user_dao(self):
        pass

    @abstractmethod
    def get_space_dao(self):
        pass

    @abstractmethod
    def get_application_dao(self):
        pass

    @abstractmethod
    def get_stats_dao(self):
        pass
