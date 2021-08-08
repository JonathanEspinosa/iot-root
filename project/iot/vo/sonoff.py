import json
from iot.vo.wifi import WifiVO


class SonoffVO:
    def __init__(self, js=None):
        if js is not None:
            jsonConvert = json.loads(js)
            self.__dict__ = jsonConvert
            self.Wifi = WifiVO(json.dumps(jsonConvert["Wifi"]))

    Time: str
    Uptime: str
    UptimeSec: str
    Heap: str
    SleepMode: str
    Sleep: str
    LoadAvg: str
    MqttCount: str
    POWER: str
    Wifi = WifiVO()
