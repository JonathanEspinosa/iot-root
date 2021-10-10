import json


class DeviceVO:
    def __init__(self, js=None):
        if js is not None:
            jsonConvert = json.loads(js)
            self.__dict__ = jsonConvert

    devicecode: int
    groupcode: int
    typecode: int
    name: str
    status: bool
    