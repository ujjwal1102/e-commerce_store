
from django.urls import path
from . import views
from django.urls import path, include,re_path

urlpatterns = [
    path('my-cart',views.AddToCartView.as_view(),name='my_cart_add'),
    path('cartview',views.CartView.as_view(),name='mycartview'),
    path('remove-from-cart',views.RemoveFromCartView.as_view(),name='removefromcart'),
    

]