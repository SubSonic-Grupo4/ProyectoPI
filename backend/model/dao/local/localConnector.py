import json
from pathlib import Path


class LocalConnector:
    def __init__(self):
        self.base_path = Path(__file__).resolve().parents[3] / "data"

    def read_json(self, filename):
        path = self.base_path / filename
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)

    def write_json(self, filename, data):
        path = self.base_path / filename
        with open(path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
