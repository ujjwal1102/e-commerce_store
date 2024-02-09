
from django.urls import path
from cart import views

urlpatterns = [
    path('cart',view=views.CartAPIView.as_view()),
]