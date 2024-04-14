from django.urls import path
# from .views import PaymentAPI, StripeCheckoutPaymentView, CreatePayment
from . import views

app_name = 'orders'
urlpatterns = [
    path('orders/', views.OrdersAPIView.as_view(),),
    path('create-checkout-session/', views.PayGateway.as_view()),
    path('success/', views.handle_payment_success, name='success'),
    path('cancel/', views.handle_payment_cancel, name='cancel'),
    path("export-orders-excel/", views.ExportOrdersExcel.as_view()),
]
