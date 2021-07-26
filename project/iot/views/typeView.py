from iot.serializer.typeSerializer import TypeSerializer
from iot.models.Type import Type
from rest_framework.generics import ListAPIView


class TypeListView(ListAPIView):
    serializer_class = TypeSerializer
    permission_classes = ()
    queryset = Type.objects.all()
