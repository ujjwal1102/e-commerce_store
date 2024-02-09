from django.urls import path
from .views import PaymentAPI,StripeCheckoutPaymentView

urlpatterns = [
    path('make_payment/', PaymentAPI.as_view(), name='make_payment'),
    # path('stripe-checkout-payment/',CreateStripeCheckoutSessionView.as_view()),
    path('stripe-checkout-payment/',StripeCheckoutPaymentView.as_view())
]