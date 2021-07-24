from django.urls import path
from Modulos.Gestion.views import GroupView
urlpatterns=[
    path('groups/',GroupView.as_view(), name='groups_list' ),
    path('groups/<int:groupcode>',GroupView.as_view(), name='groups_process' ),
]