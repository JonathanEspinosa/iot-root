import json


class WifiVO:
    def __init__(self, js=None):
        if js is not None:
            jsonConvert = json.loads(js)
            self.__dict__ = jsonConvert

    AP: str
    SSId: str
    BSSId: str
    Channel: str
    RSSI: str
    Signal: str
    LinkCount: str
    Downtime: str
