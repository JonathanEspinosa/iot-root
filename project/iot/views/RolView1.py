from iot.models.Rol import Rol
from iot.serializer.rolSerializer import RolSerializer
from rest_framework.generics import ListAPIView


class RolListView(ListAPIView):
    serializer_class = RolSerializer
    permission_classes = ()
    queryset = Rol.objects.all()

