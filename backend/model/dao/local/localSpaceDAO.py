from backend.model.dao.local.localConnector import LocalConnector
from backend.model.dto.spaceDTO import SpaceDTO


class LocalSpaceDAO:
    def __init__(self):
        self.connector = LocalConnector()
        self.filename = "spaces.json"

    def get_spaces(self, tipo=None, only_available=False):
        spaces = self.connector.read_json(self.filename)
        filtered = []
        for space in spaces:
            if tipo and space["tipo"].upper() != tipo.upper():
                continue
            if only_available and not space["disponible"]:
                continue
            filtered.append(SpaceDTO(**space))
        return filtered

    def get_space_by_id(self, id_espacio):
        spaces = self.connector.read_json(self.filename)
        for space in spaces:
            if space["idEspacio"] == id_espacio:
                return SpaceDTO(**space)
        return None
