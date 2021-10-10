import json
from typing import List

from iot.vo.rolSelect import RolSelectVO


class UserVO:
    def __init__(self, js=None):
        if js is not None:
            jsonConvert = json.loads(js)
            self.__dict__ = jsonConvert

    usercode: int
    username: str
    password: str
    name: str
    email: str
    phone: str
    status: bool
    rolList: List[RolSelectVO] 
