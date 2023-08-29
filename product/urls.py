
from django.urls import path
from . import views
from django.urls import path, include,re_path

urlpatterns = [
    path('add-product-view',views.AddProductView.as_view(),name='add_prod'),
    path('all-product-view',views.ProductListView.as_view(),name='all_prod'),
    path('product-detail-view/<pk>',views.ProductDetailView.as_view(),name='prod_detail'),
    ]