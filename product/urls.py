
from django.urls import path
from . import views
# from django.urls import path, include,re_path

urlpatterns = [
    path('products', view=views.ProductsAPIView.as_view()),
    path('seller/products', view=views.SellerProductListAPIView.as_view()),
    path('seller/products', view=views.SellerProductUpdateAPIView.as_view()),
    path('seller/product/<int:pk>',
         view=views.SellerProductRetrieveAPIView.as_view()),
    path('product/<int:pk>', views.ProductRetrieveAPIView.as_view()),
    path('shop', view=views.ShopView.as_view()),
    path('homeshop',views.HomeShopAPIView.as_view()),
    path('shop/<int:id>',views.ShopCategoryAPIView.as_view()),
    path('brands',view=views.BrandAPIView.as_view()),
]
