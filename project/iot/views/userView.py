import json
import jsonpickle
from iot.serializer.userSerializer import UserSerializer
from rest_framework.generics import ListAPIView
from django.http.response import JsonResponse
from rest_framework.views import APIView
from django.db.models import Max
from rest_framework import status
from iot.models.User import User
from iot.vo.genericResponse import GenericResponse
from iot.vo.user import UserVO


class Create(APIView):
    def post(self, request, format=None):
        userVO = UserVO(json.dumps(request.data))
        valObj = User.objects.filter(username=userVO.username).first()
        response = GenericResponse()
        if valObj != None:
            repeatedName = getattr(valObj, "username")
            response.error = 1
            response.message = (
                "Ya existe un usuario registrado con el nombre '"
                + repeatedName
                + "' por favor cambielo"
            )
            return JsonResponse(
                json.loads(jsonpickle.encode(response)), status=status.HTTP_201_CREATED
            )
        else:
            userVO.usercode = (
                0
                if User.objects.aggregate(Max("usercode"))["usercode__max"] is None
                else User.objects.aggregate(Max("usercode"))["usercode__max"]
            ) + 1
            userVO.status = True
            user_serializer = UserSerializer(data=json.loads(jsonpickle.encode(userVO)))
            if user_serializer.is_valid():
                user_serializer.save()
                response.error = 0
                response.message = ""
                return JsonResponse(
                    json.loads(jsonpickle.encode(response)),
                    status=status.HTTP_201_CREATED,
                )
            return JsonResponse(
                user_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )


class Update(APIView):
    def post(self, request, format=None):
        userVo = UserVO(request.body)
        valObj = (
            User.objects.filter(username=userVo.username)
            .exclude(usercode=userVo.usercode)
            .first()
        )
        response = GenericResponse()
        if valObj != None:
            repeatedName = getattr(valObj, "username")
            response.error = 1
            response.message = (
                "Ya existe un usuario registrado con el nombre '"
                + repeatedName
                + "' por favor cambielo"
            )
            return JsonResponse(
                json.loads(jsonpickle.encode(response)), status=status.HTTP_201_CREATED
            )
        else:
            retrieveObj = User.objects.get(usercode=userVo.usercode)
            user_serializer = UserSerializer(
                retrieveObj, data=json.loads(jsonpickle.encode(userVo))
            )
            if user_serializer.is_valid():
                user_serializer.save()
                response.error = 0
                return JsonResponse(
                    json.loads(jsonpickle.encode(response)),
                    status=status.HTTP_201_CREATED,
                )
            return JsonResponse(
                user_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )


# Lista los todos los usuarios para front
class ListAll(ListAPIView):
    serializer_class = UserSerializer
    permission_classes = ()
    queryset = User.objects.all()
