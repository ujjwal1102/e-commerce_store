# from typing import Any, Dict
# from django.db.models.query import QuerySet
# from django.http import HttpRequest, HttpResponse,JsonResponse
# from django.shortcuts import render,redirect
# from django.views import View
# # Create your views here.
# from django.views.generic import ListView
# from django.views.generic.base import TemplateView
# from django.views.generic.edit import CreateView,ModelFormMixin
# from product.models import Product
# # from django.
# from product.models import Product
# from django.contrib.sessions.models import Session

import json
from typing import Any
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.models import Session
from product.models import Product
from product.serializers import ProductSerializer
from django.shortcuts import get_object_or_404

def calc_cart_items(cart_items):
    total_cost = 0
    cart_products = []
    print(cart_items['cart_items'])
    try:
        for item in cart_items['cart_items']:
            product = Product.objects.get(id=item['id'])
            cart_products.append(ProductSerializer(product).data)
            total_cost = round(total_cost +(product.cost * int(item['quantity'])),2)
            print(item['id'],'product.cost : ',product.cost,"total_cost : ",total_cost,"cart_products : ",cart_products)
        print('total_cost : ',total_cost)  
    except:
        pass
    return (total_cost,cart_items,cart_products)

class CartAPIView(APIView):
    pass


    def post(self, request, format=None):
        cart_items= self.request.data
        (total_cost,cart_items,cart_products) = calc_cart_items(cart_items=cart_items)
        
        return Response(data={"cart": cart_items,'total_cost':total_cost,"cart_products":cart_products}, status=status.HTTP_200_OK)


class CheckOutView(APIView):
    def get(self,request,format=None):pass
    def post(self,request,format=None):pass
    def update(self,request,format=None):pass
    def delete(self,request,format=None):pass
