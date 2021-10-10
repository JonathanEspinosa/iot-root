import json


class DeviceSelectVO:
    def __init__(self, js=None):
        if js is not None:
            jsonConvert = json.loads(js)
            self.__dict__ = jsonConvert

    devicecode: int
    name: str
    groupname: str
    status: bool
    