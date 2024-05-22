from django.urls import path
from . import views

urlpatterns = [
    path("products", view=views.ProductsAPIView.as_view()),
    path("seller/products", view=views.SellerProductListAPIView.as_view()),
    path("seller/product/<int:pk>", view=views.SellerProductRetrieveAPIView.as_view()),
    path("product/<int:pk>", views.ProductRetrieveAPIView.as_view()),
    path("shop", view=views.ShopView.as_view()),
    path("homeshop", views.HomeShopAPIView.as_view()),
    path("shop/<int:id>", views.ShopCategoryAPIView.as_view()),
    path("brands", view=views.BrandAPIView.as_view()),
    path("products/review",view=views.ProductReviewListCreateView.as_view()),
    path("products/review/<int:pk>",view=views.ProductReviewListCreateView.as_view()),
    # path("products/reviews",view=views.ProductReviewDetailView.as_view()),
]
