from django.middleware.common import MiddlewareMixin
from .models import ProductWishlist
class WishlistMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
        

    def __call__(self, request):
       
        user = request.user.id
        print(list(ProductWishlist.objects.filter(user=user).values_list('product',flat=True)))
        if request.user.is_authenticated:
            request.session.setdefault('wishlist',{})
            request.session['wishlist'] = list(ProductWishlist.objects.filter(user=user).values_list('product',flat=True))
        # request['dictionary'] = ProductWishlist.objects.filter(user=user).values_list('product')
        response = self.get_response(request)
        return response
   
