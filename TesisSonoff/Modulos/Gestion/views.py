from django.http.response import JsonResponse
from django.views import View
from .models import GROUP, models
# Create your views here.
class GroupView(View):
    def  get(self,request):
         groups= list(GROUP.objects.values()) 
         
         if len(groups)>0:
             datos={'message':"Success",'groups':groups}
         else:
             datos={'message':"Groups not found..."}
         return JsonResponse(datos)  
    def  post(self,request):
         pass
    def  put(self,request):
         pass
    def  delete(self,request):
         pass

