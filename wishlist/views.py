from typing import Any, Dict
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from .models import ProductWishlist
# Create your views here.
from django.views.generic.list import ListView
from django.views import View
from django.http import JsonResponse,HttpResponse
# from django.views.generic.edit import CreateView,UpdateView,DeleteView
# from django.shortcuts import render, redirect
# from django.views.decorators.csrf import csrf_exempt
import json

class WishlistView(ListView):
    model = ProductWishlist
    template_name = 'wishlist/wishlist.html'
        
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        print('context :',context)
        return context

class AddToWishlist(View):
    
    def post(self,*args, **kwargs):
        prod_id = self.request.POST.get('product_id')
        user = self.request.user
        print('prod_id :-',prod_id,'-','user-:-',user,'-')
        wishlist, created = ProductWishlist.objects.get_or_create(user=user, product_id=prod_id)
        print(' wishlist : ', wishlist,'created : ',created)
        if created:
            status = 'bi-heart-fill'
            prod_id = prod_id
            # self.request.session['wishlist'] = ProductWishlist.objects.filter(user=user).values_list('product',flat=True)
        else:
            wishlist.delete()
            status = 'bi-heart'
            prod_id=prod_id
            print('prod_id : ',prod_id)
        return JsonResponse({'status':status,'prod_id': prod_id})
    
