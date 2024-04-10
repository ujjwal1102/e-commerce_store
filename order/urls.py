from django.urls import path
# from .views import PaymentAPI, StripeCheckoutPaymentView, CreatePayment
from . import views

app_name = 'orders'
urlpatterns = [
    # path('make_payment/', PaymentAPI.as_view(), name='make_payment'),
    # path('stripe-checkout-payment/', views.PayGateway.as_view()),
    path('orders/', views.OrdersAPIView.as_view(),),
    path('create-checkout-session/', views.PayGateway.as_view()),
    # path('stripe-checkout-payment/', StripeCheckoutPaymentView.as_view()),
    # path('create/', views.CreatePaymentView.as_view(), name='create_payment'),
    # path('confirm/', views.ConfirmPaymentView.as_view(), name='confirm_payment'),
    path('success/', views.handle_payment_success, name='success'),
    path('cancel/', views.handle_payment_cancel, name='cancel'),
    path("export-orders-excel/", views.ExportOrdersExcel.as_view()),
    # path('create-payment-intent', CreatePayment.as_view()),
]
