import json


class RolSelectVO:
    def __init__(self, js=None):
        if js is not None:
            jsonConvert = json.loads(js)
            self.__dict__ = jsonConvert

    rolcode: int
    name: str
    description: str
    status: bool
    