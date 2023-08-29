from django.urls import path
from . import views
from django.urls import path, include,re_path

urlpatterns = [
    path('add',views.AddToWishlist.as_view(),name='add_to_wishlist'),
    path('my-wishlist',views.WishlistView.as_view(),name='my_wishlist'),
    
    ]