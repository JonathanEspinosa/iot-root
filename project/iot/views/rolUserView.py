import json
from typing import List
from django.http.response import JsonResponse
import jsonpickle
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from iot.models import RolUser
from iot.vo.rolSelect import RolSelectVO
from iot.serializer.rolUserSerializer import RolUserSerializer
from iot.vo.genericResponse import GenericResponse
from iot.vo.rolUser import RolUserVO
from iot.vo.user import UserVO


# Lista todos los roles de un usuario
class ListRolByUser(APIView):
    def get(self, request, usercode):
        responseList: List[RolSelectVO] = []
        for rol in RolUser.objects.filter(usercode=usercode).filter(status=True):
            rolAux = getattr(rol, "rolcode")
            resp = RolSelectVO()
            resp.rolcode = getattr(rolAux, "rolcode")
            resp.name = getattr(rolAux, "name")
            resp.description = getattr(rolAux, "description")
            resp.status = getattr(rol, "status")
            responseList.append(resp)
        return Response(json.loads(jsonpickle.encode(responseList)))


class Configure(APIView):
    def post(self, request, format=None):
        userVO = UserVO(json.dumps(request.data))
        response = GenericResponse()
        response.error = 0
        for item in userVO.rolList:
            rol = RolSelectVO(json.dumps(item))
            rolUserCurrent = (
                RolUser.objects.filter(usercode=userVO.usercode)
                .filter(rolcode=rol.rolcode)
                .first()
            )
            if rolUserCurrent is None and rol.status:
                rolUserVO = RolUserVO()
                rolUserVO.usercode = userVO.usercode
                rolUserVO.rolcode = rol.rolcode
                rolUserVO.status = True
                rolUser_serializer = RolUserSerializer(
                    data=json.loads(jsonpickle.encode(rolUserVO))
                )
                if rolUser_serializer.is_valid():
                    rolUser_serializer.save()
                else:
                    response.error = 1
                    response.message = response.message + rolUser_serializer.errors
            else:
                if (
                    rolUserCurrent is not None
                    and getattr(rolUserCurrent, "status") != rol.status
                ):
                    rolUserVO = RolUserVO()
                    rolUserVO.usercode = userVO.usercode
                    rolUserVO.rolcode = rol.rolcode
                    rolUserVO.status = rol.status
                    rolUser_serializer = RolUserSerializer(
                        rolUserCurrent,
                        data=json.loads(jsonpickle.encode(rolUserVO)),
                    )
                    if rolUser_serializer.is_valid():
                        rolUser_serializer.save()
                    else:
                        response.error = 1
                        response.message = response.message + rolUser_serializer.errors
        return JsonResponse(
            json.loads(jsonpickle.encode(response)),
            status=status.HTTP_201_CREATED,
        )
