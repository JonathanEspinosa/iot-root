from io import StringIO
import json
from json.encoder import JSONEncoder
from typing import List
from django.db.models.fields import CommaSeparatedIntegerField
from django.http.response import JsonResponse
from django.utils.decorators import method_decorator
from django.utils.regex_helper import Group
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from .models import GROUP, models 
import json
# Create your views here.
class GroupView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
         return super().dispatch(request, *args, **kwargs)
    def  get(self, request, groupcode=0):
         if (groupcode>0):
               groups = list(GROUP.objects.filter(groupcode=groupcode).values())
               if len(groups) > 0:
                   Group=groups[0]
                   datos={'message':"Success",'groups':Group}
               else: 
                   datos={'message':"Groups not found..."}
               return JsonResponse(datos)
         else:
               groups = list(GROUP.objects.values()) 
               if len(groups) > 0:
                    datos={'message':"Success",'groups':groups}
               else:
                    datos={'message':"Groups not found..."}
               return JsonResponse(datos)
    def  post(self,request): 
         #print(request.body)#enviado el json para que se registre
         jd=json.loads(request.body)
        # print(jd)
         GROUP.objects.create(groupcode=jd['groupcode'],name=jd['name'],status=jd['status'])
         datos = {'message': "Success"}
         return JsonResponse(datos)
    def  put(self,request):
         pass
    def  delete(self,request):
         pass

