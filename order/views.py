from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CardInformationSerializer
import stripe
from rest_framework import status
from django.conf import settings
import logging

class PaymentAPI(APIView):
    serializer_class = CardInformationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        response = {}
        if serializer.is_valid():
            data_dict = serializer.data

            stripe.api_key = settings.STRIPE_SECRET_KEY  # 'your-key-goes-here'
            response = self.stripe_card_payment(data_dict=data_dict)

        else:
            response = {'errors': serializer.errors, 'status':
                        status.HTTP_400_BAD_REQUEST
                        }

        return Response(response)

    def stripe_card_payment(self, data_dict):
        try:
            card_details = {
                "type": "card",
                "card": {
                    "number": data_dict['card_number'],
                    "exp_month": data_dict['expiry_month'],
                    "exp_year": data_dict['expiry_year'],
                    "cvc": data_dict['cvc'],
                },
            }
            #  you can also get the amount from databse by creating a model
            payment_intent = stripe.PaymentIntent.create(
                amount=10000,
                currency='inr',
            )
            payment_intent_modified = stripe.PaymentIntent.modify(
                payment_intent['id'],
                payment_method=card_details['id'],
            )
            try:
                payment_confirm = stripe.PaymentIntent.confirm(
                    payment_intent['id']
                )
                payment_intent_modified = stripe.PaymentIntent.retrieve(
                    payment_intent['id'])
            except:
                payment_intent_modified = stripe.PaymentIntent.retrieve(
                    payment_intent['id'])
                payment_confirm = {
                    "stripe_payment_error": "Failed",
                    "code": payment_intent_modified['last_payment_error']['code'],
                    "message": payment_intent_modified['last_payment_error']['message'],
                    'status': "Failed"
                }
            if payment_intent_modified and payment_intent_modified['status'] == 'succeeded':
                response = {
                    'message': "Card Payment Success",
                    'status': status.HTTP_200_OK,
                    "card_details": card_details,
                    "payment_intent": payment_intent_modified,
                    "payment_confirm": payment_confirm
                }
            else:
                response = {
                    'message': "Card Payment Failed",
                    'status': status.HTTP_400_BAD_REQUEST,
                    "card_details": card_details,
                    "payment_intent": payment_intent_modified,
                    "payment_confirm": payment_confirm
                }
        except:
            response = {
                'error': "Your card number is incorrect",
                'status': status.HTTP_400_BAD_REQUEST,
                "payment_intent": {"id": "Null"},
                "payment_confirm": {'status': "Failed"}
            }
        return response




stripe.api_key = settings.STRIPE_SECRET_KEY

class StripeCheckoutPaymentView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            price =1000

            checkout_session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[
                    {
                        "price_data": {
                            "currency": "usd",
                            "unit_amount": int(price) * 100,
                            "product_data": {
                                "name": "Test Product Name",
                                "description": "Test Product Description",
                                # "images": [
                                #     f"{settings.BACKEND_DOMAIN}/{price.product.thumbnail}"
                                # ],
                            },
                        },
                        "quantity": 5,
                    }
                ],
                metadata={"product_id": 12323423455676},
                mode="payment",
                success_url=settings.PAYMENT_SUCCESS_URL,
                cancel_url=settings.PAYMENT_CANCEL_URL,
            )
            return Response(data={"url":checkout_session.url},status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(data={"exception":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
    # def post(self, request, *args, **kwargs):
    #     try:
    #         total_price = int(request.data.get('total_price'))
    #         card_name = request.data.get('card_name')
    #         payment_method_id = request.data.get('payment_method_id')
    #         success_url = "http://localhost:3000/success"  # Specify your success URL
    #         cancel_url = "http://localhost:3000/cancel"

    #         payment_method = stripe.PaymentMethod.create(
    #             type="card",
    #             card={"token": payment_method_id},
    #             billing_details={
    #                 "name": card_name,
    #             },
    #         )

    #         # Confirm the PaymentIntent using the Payment Method
    #         payment_intent = stripe.PaymentIntent.create(
    #             amount=total_price,
    #             currency='usd',
    #             payment_method=payment_method.id,
    #             confirmation_method='manual',
    #             confirm=True,
    #             return_url=success_url,
    #         )
    #         if payment_intent.status == 'succeeded':
    #             # Add your logic to handle a successful payment
    #             return Response({"message": "Payment successful"}, status=status.HTTP_200_OK)
    #         else:
    #             print(payment_intent.status)
    #             # Handle other payment statuses (e.g., requires_action, requires_payment_method, etc.)
    #             return Response({"error": "Payment failed"}, status=status.HTTP_400_BAD_REQUEST)

    #     except stripe.error.CardError as e:
    #         # Handle card errors
    #         return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

     
    #     except Exception as e:
    #         print(e)
    #         # Something else happened
    #         return Response({"error": "Internal server error", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





# logger = logging.getLogger(__name__)

# class StripeCheckoutPaymentView(APIView):
#     def post(self, request, *args, **kwargs):
#         try:
#             total_price = int(request.data.get('total_price'))
#             card_name = request.data.get('card_name')
#             payment_method_id = request.data.get('payment_method_id')

#             # Validate and sanitize input data
#             if total_price <= 0:
#                 return Response({"error": "Invalid total_price"}, status=status.HTTP_400_BAD_REQUEST)

#             success_url = settings.STRIPE_SUCCESS_URL
#             # cancel_url = settings.STRIPE_CANCEL_URL
#             export_description = "Description for export transaction"
#             # Use payment_method_id directly
#             customer_name = "Ujjwal Srivastava"
#             customer_address = "This is just a demo address"
            
#             export_customer_details = {
#                 'name': customer_name,
#                 'address': {
#                     'line1': customer_address,
#                     # Add additional address fields as needed
#                 },
#             }
#             payment_intent = stripe.PaymentIntent.create(
#                 amount=total_price,
#                 currency='usd',
#                 payment_method=payment_method_id,
#                 confirmation_method='automatic',
#                 confirm=True,
#                 return_url=success_url,
#                 description=export_description,
#                 customer=customer_address,
#             )

#             if payment_intent.status == 'succeeded':
#                 return Response({"message": "Payment successful"}, status=status.HTTP_200_OK)
#             elif payment_intent.status == 'requires_action':
#                 # Additional step needed to authenticate the payment
#                 return Response({"requires_action": True, "payment_intent_client_secret": payment_intent.client_secret})
#             else:
#                 logger.error(f"Payment failed: {payment_intent.status}")
#                 return Response({"error": "Payment failed"}, status=status.HTTP_400_BAD_REQUEST)

#         except stripe.error.CardError as e:
#             logger.error(f"Card error: {str(e)}")
#             return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

#         except Exception as e:
#             logger.exception(f"Internal server error: {str(e)}")
#             return Response({"error": "Internal server error", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





   # except stripe.error.CardError as e:
        #     # Since it's a decline, stripe.error.CardError will be caught
        #     print(e)
        #     body = e.error.payment_intent
        #     return Response({"error": str(body)}, status=status.HTTP_400_BAD_REQUEST)
        # except stripe.error.RateLimitError as e:
        #     # Too many requests made to the API too quickly
        #     print(e)
        #     return Response({"error": "Rate limit error"}, status=status.HTTP_429_TOO_MANY_REQUESTS)
        # except stripe.error.InvalidRequestError as e:
        #     # Invalid parameters were supplied to Stripe's API
        #     print(e)
        #     return Response({"error": "Invalid parameters"}, status=status.HTTP_400_BAD_REQUEST)
        # except stripe.error.AuthenticationError as e:
        #     # Authentication with Stripe's API failed
        #     print(e)
        #     return Response({"error": "Authentication failed"}, status=status.HTTP_401_UNAUTHORIZED)
        # except stripe.error.APIConnectionError as e:
        #     # Network communication with Stripe failed
        #     print(e)
        #     return Response({"error": "API connection error"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        # except stripe.error.StripeError as e:
        #     # Generic error handling
        #     print(e)
        #     return Response({"error": "Payment failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)