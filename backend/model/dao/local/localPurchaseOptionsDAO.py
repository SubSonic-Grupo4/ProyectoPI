from backend.model.dao.local.localConnector import LocalConnector
from backend.model.dto.purchaseOptionsDTO import PurchaseOptionsDTO


class LocalPurchaseOptionsDAO:
    def __init__(self):
        self.connector = LocalConnector()
        self.filename = "purchaseOptions.json"

    def get_purchase_options(self):
        data = self.connector.read_json(self.filename)
        return PurchaseOptionsDTO(
            events=data.get("events", []),
            passes=data.get("passes", [])
        )
