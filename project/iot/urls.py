from iot.views.deviceView import DeviceListView
from iot.views.typeView import TypeListView
from iot.views.groupView import GroupListView
from django.urls import path

urlpatterns = [
    # Web service group table
    path("group/", GroupListView.as_view(), name="group"),
    # Web service type table
    path("type/", TypeListView.as_view(), name="type"),
    # Web service device table
    path("device/", DeviceListView.as_view(), name="device"),
    path("publish/", DeviceListView.as_view(), name="publish"),
    # path("device/{consultaVO}", DeviceListView.as_view(), name="device"),
]
