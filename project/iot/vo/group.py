import json


class GroupVO:
    def __init__(self, js=None):
        if js is not None:
            jsonConvert = json.loads(js)
            self.__dict__ = jsonConvert

    fathercode: int
    groupcode: int
    name: str
    status: bool
