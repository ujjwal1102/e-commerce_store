from typing import Any, Dict
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse,JsonResponse
from django.shortcuts import render,redirect
from django.views import View
# Create your views here.
from django.views.generic import ListView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView,ModelFormMixin
from product.models import Product
# from django.
from product.models import Product
from django.contrib.sessions.models import Session 

def cart_item_count(cart):
  return sum([int(value) for value in cart.values()])
  
def total_calculate_price_of_product(mycart):
  total_cost = 0
  print('mycart',mycart,type(mycart))
  for prod_id,quantity in mycart.items():
    print(prod_id,quantity)
    prod = Product.objects.get(id=prod_id)
    print(prod)
    prod_cost = prod.cost
    print(prod_cost)
    item_total_cost = prod_cost*int(quantity)
    print('item_total_cost',item_total_cost)
    total_cost += item_total_cost
    print('total_cost',total_cost)
  return total_cost

class RemoveFromCartView(View):
  def post(self, *args, **kwargs):
    pid = self.request.POST.get('product_id')
    print(' pid', pid)
    del self.request.session['mycart'][pid]
    total_cost = total_calculate_price_of_product(mycart=self.request.session['mycart'])
    cartviewcount = cart_item_count(cart=self.request.session['mycart'])
    return JsonResponse({'mycart' : f'{self.request.session["mycart"]}','total_cost':f'{total_cost}','product_id':str(pid),'count':str(cartviewcount)})
class AddToCartView(View):
  
  def post(self, *args, **kwargs) :
    pid = self.request.POST.get('product_id')
    quantity = self.request.POST.get('quantity')
    print(Session.objects)
    print('pid : ',pid,'quantity : ',quantity)
    cart = self.request.session.get('mycart',{})
    cart[int(pid)] = int(quantity)
    print(cart)
    count = cart_item_count(cart)
    # count = sum([int(value) for value in cart.values()])
    self.request.session['mycart'] = cart
    print(self.request.session['mycart']) 
    print(cart,self.request.session.keys())
    self.request.session['count'] = count
    print('count',count)
    total_cost = total_calculate_price_of_product(mycart=self.request.session['mycart'])  
    return JsonResponse({'status':'Added to cart','cartviewcount':str(count),'mycart' : f'{self.request.session["mycart"]}','total_cost':f'{total_cost}','product_id':str(pid)}) 

class CartView(ListView):
  model = Session
  template_name = 'cart/cartview.html'

  def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
    context = super().get_context_data(**kwargs)
    if self.request.session.has_key('mycart'):
      products = []
      context['mycart'] = self.request.session['mycart']   
      no_of_products = None
      print(type(self.request.session['mycart']))
      for s,p in self.request.session['mycart'].items():
          print(s,p)
          products.append((Product.objects.get(id=s),p))
      no_of_products = products.count
      print(products)
      context['products'] = products
      context['no_of_products'] = no_of_products
      total_cost = total_calculate_price_of_product(mycart=self.request.session['mycart'])
      context['total_cost'] = f'{total_cost}'
    print(context)
    return context

  def get_queryset(self) -> QuerySet[Any]:
    context = super().get_queryset()
    print('context : ',context)
    return context
  # def form_valid(self, form):
    
  #   # Get the product from the database.
  #   product = Product.objects.get(id=form.cleaned_data['product_id'])

  #   # Add the product to the cart.
  #   session = self.request.session
  #   session['mycart'] = {} if 'mycart' not in session else session['mycart']
  #   session['mycart'][product] = {
  #     'quantity': form.cleaned_data['quantity'],
  #     'price': product.price
  #   }

  #   # Save the cart to the session.
  #   session.modified = True

  #   return super().form_valid(form)