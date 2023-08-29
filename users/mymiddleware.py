
from django.http import HttpResponseForbidden,Http404
from django.core.exceptions import PermissionDenied
from .models import Product
class MyMiddleware:
    
    def __init__(self,get_response):
        # print(get_response)
        self.get_response = get_response
        print('__init__')
        # print(self.get_response.data)
        
    def __call__(self,request):
        #print('Before View')
        
        response = self.get_response(request)
        
        self.check_type(request)
        print('After View')
        #print(request.META['QUERY_STRING'])
        return response
    
    def check_type(self,request):
        if (not request.user.is_superuser) and (not request.user.is_staff):
            if (request.path == '/add-new-product') or (request.path == '/category'):
               # raise Http404('Url unaccessible')
               raise PermissionDenied()
        
        if request.user.is_anonymous:
            if '/add-to-cart'  in request.path or '/cart' in request.path :
                print(type(request.path),request.user.is_anonymous)
                raise PermissionDenied()
    
    
            