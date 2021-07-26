from iot.views.deviceView import DeviceListView
from iot.views.typeView import TypeListView
from iot.views.groupView import GroupListView
from django.urls import path

urlpatterns = [
    path("group/", GroupListView.as_view(), name="group"),
    path("type/", TypeListView.as_view(), name="type"),
    path("device/", DeviceListView.as_view(), name="device"),
]
