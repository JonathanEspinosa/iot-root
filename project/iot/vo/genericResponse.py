import json

class GenericResponse:
    def __init__(self, js=None):
        if js is not None:
            jsonConvert = json.loads(js)
            self.__dict__ = jsonConvert

    error: int
    message: str
