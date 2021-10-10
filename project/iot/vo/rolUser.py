import json
from typing import List
from iot.vo.deviceSelect import DeviceSelectVO


class RolUserVO:
    def __init__(self, js=None):
        if js is not None:
            jsonConvert = json.loads(js)
            self.__dict__ = jsonConvert

    rolcode: int
    usercode: int
    status: bool
