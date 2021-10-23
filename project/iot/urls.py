
from iot.views import groupView, typeView, deviceView, userView, rolView, rolUserView,deviceAllView,deviceGroupView,groupidView,loginView,onoff,rolDeviceAllView,rolDeviceView,rolUser1View, RolView1
from django.urls import path





urlpatterns = [
    # Web service type table
    path("type/", typeView.TypeListView.as_view(), name="type"),
    path("type/test", typeView.testApiView.as_view(), name="type"),
    # Web service group table
    path("group/create", groupView.Create.as_view(), name="group"),
    path("group/update", groupView.Update.as_view(), name="group"),
    path(
        "group/findTableByCode/<groupcode>",
        groupView.FindTableByCode.as_view(),
        name="group",
    ),
    path(
        "group/filterTableByFather/<fathercode>",
        groupView.FilterTableByFather.as_view(),
        name="group",
    ),
    # Web service device table
    path("device/listAllDevice", deviceView.ListAll.as_view(), name="device"),
    path("device/create", deviceView.Create.as_view(), name="device"),
    path("device/update", deviceView.Update.as_view(), name="device"),
    path(
        "device/filterTableByGroupCode/<groupcode>",
        deviceView.FilterTableByGroupCode.as_view(),
        name="device",
    ),
    # Web service user table
    path("user/create", userView.Create.as_view(), name="user"),
    path("user/update", userView.Update.as_view(), name="user"),
    path("user/listAll", userView.ListAll.as_view(), name="user"),
    # Web service rol table
    path("rol/create", rolView.Create.as_view(), name="rol"),
    path("rol/update", rolView.Update.as_view(), name="rol"),
    path("rol/listAll", rolView.ListAll.as_view(), name="rol"),
    path("rol/listAllActive", rolView.ListAllActive.as_view(), name="rol"),
    # Web service rol device table
    path("rolUser/listRolByUser/<usercode>", rolUserView.ListRolByUser.as_view(), name="rolUser"),
    path("rolUser/configure", rolUserView.Configure.as_view(), name="rolUser"),
    path("user/<str:username>,<str:password>",loginView.Login.as_view(), name= "user"),#jessy
    path("roluser/<int:usercode>", rolUser1View.List_Rol.as_view(), name= "roluser"),#jessy
    path("rol/", RolView1.RolListView.as_view(), name= "rol"),#jessy
    path("roldevice/<int:rolcode>", rolDeviceView.List_RolDevice.as_view(), name= "roldevice"),#jessy
    path("device/<int:devicecode>", deviceGroupView.List_GroupDevice.as_view(), name= "device"),#jessy
    path("deviceonoff/<str:name>", onoff.OnoffApiView.as_view(), name="on/off"),
    path("listroldevice/", rolDeviceAllView.RolDeviceAlltView.as_view(), name="roldevice"),
    path("deviceall/", deviceAllView.DeviceAllView.as_view(), name="alldevice"),
    path("groupid/<int:groupcode>", groupidView.GroupidListView.as_view(), name="groupid"),


]
