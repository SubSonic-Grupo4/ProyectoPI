class PurchaseOptionsDTO:
    def __init__(self, events, passes):
        self.events = events
        self.passes = passes

    def to_dict(self):
        return {
            "events": self.events,
            "passes": self.passes
        }
