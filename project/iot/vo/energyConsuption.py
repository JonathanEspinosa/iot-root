import json
from datetime import date

class EnergyConsuptionVO:
    def __init__(self, js=None):
        if js is not None:
            jsonConvert = json.loads(js)
            self.__dict__ = jsonConvert

    eneconcode: int
    groupcode: int
    date:  str
    energyday: float
    