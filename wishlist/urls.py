from django.urls import path
from . import views
# from django.urls import path, include,re_path

urlpatterns = [
    path('wishlist',view=views.WishlistAPIView.as_view()),
    path('wishlist/add',view=views.WishlistAPIView.as_view()),
    path('wishlist/<int:id>/update',view=views.WishlistAPIView.as_view()),
    path('wishlist/delete',view=views.WishlistAPIView.as_view()),
    
    
    ]