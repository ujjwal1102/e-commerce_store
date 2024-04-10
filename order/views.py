from .serializers import PaymentSerializer
from django.shortcuts import render, redirect
from django.http import FileResponse
# Create your views here.
from django.urls import reverse
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CardInformationSerializer
import stripe
from rest_framework import status
from django.conf import settings
import logging
from django.http import JsonResponse
from .models import Order
import json
from .serializers import OrderSerializer
from users.models import Customer
from django.views.decorators.csrf import csrf_exempt
from product.models import Product
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from excel_response import ExcelResponse
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, permissions
# class PaymentAPI(APIView):
#     serializer_class = CardInformationSerializer

#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         response = {}
#         if serializer.is_valid():
#             data_dict = serializer.data

#             stripe.api_key = settings.STRIPE_SECRET_KEY  # 'your-key-goes-here'
#             response = self.stripe_card_payment(data_dict=data_dict)

#         else:
#             response = {'errors': serializer.errors, 'status':
#                         status.HTTP_400_BAD_REQUEST
#                         }

#         return Response(response)

#     def stripe_card_payment(self, data_dict):
#         try:
#             card_details = {
#                 "type": "card",
#                 "card": {
#                     "number": data_dict['card_number'],
#                     "exp_month": data_dict['expiry_month'],
#                     "exp_year": data_dict['expiry_year'],
#                     "cvc": data_dict['cvc'],
#                 },
#             }
#             #  you can also get the amount from databse by creating a model
#             payment_intent = stripe.PaymentIntent.create(
#                 amount=10000,
#                 currency='inr',
#             )
#             payment_intent_modified = stripe.PaymentIntent.modify(
#                 payment_intent['id'],
#                 payment_method=card_details['id'],
#             )
#             try:
#                 payment_confirm = stripe.PaymentIntent.confirm(
#                     payment_intent['id']
#                 )
#                 payment_intent_modified = stripe.PaymentIntent.retrieve(
#                     payment_intent['id'])
#             except:
#                 payment_intent_modified = stripe.PaymentIntent.retrieve(
#                     payment_intent['id'])
#                 payment_confirm = {
#                     "stripe_payment_error": "Failed",
#                     "code": payment_intent_modified['last_payment_error']['code'],
#                     "message": payment_intent_modified['last_payment_error']['message'],
#                     'status': "Failed"
#                 }
#             if payment_intent_modified and payment_intent_modified['status'] == 'succeeded':
#                 response = {
#                     'message': "Card Payment Success",
#                     'status': status.HTTP_200_OK,
#                     "card_details": card_details,
#                     "payment_intent": payment_intent_modified,
#                     "payment_confirm": payment_confirm
#                 }
#             else:
#                 response = {
#                     'message': "Card Payment Failed",
#                     'status': status.HTTP_400_BAD_REQUEST,
#                     "card_details": card_details,
#                     "payment_intent": payment_intent_modified,
#                     "payment_confirm": payment_confirm
#                 }
#         except:
#             response = {
#                 'error': "Your card number is incorrect",
#                 'status': status.HTTP_400_BAD_REQUEST,
#                 "payment_intent": {"id": "Null"},
#                 "payment_confirm": {'status': "Failed"}
#             }
#         return response


stripe.api_key = settings.STRIPE_SECRET_KEY


# def calculate_order_amount(items):
#     return 1400


# class CreatePayment(APIView):
#     def post(self, request, *args, **kwargs):

#         try:
#             print(request.data)
#             data = request.data
#             customer = stripe.Customer.create(
#                 name="Customer",
#                 address={
#                     "line1": "510 Townsend St",
#                     "postal_code": "98140",
#                     "city": "San Francisco",
#                     "state": "CA",
#                     "country": "US",
#                 },
#             )
#             intent = stripe.PaymentIntent.create(
#                 amount=calculate_order_amount(data['items']),
#                 currency='inr',

#                 payment_method="pm_card_visa",
#                 description="This is test Description",
#                 customer=customer.id
#                 # payment_method_types=["card"],
#                 # In the latest version of the API, specifying the `automatic_payment_methods` parameter is optional because Stripe enables its functionality by default.
#                 # automatic_payment_methods={
#                 #     'enabled': True,
#                 # },
#             )
#             return Response(data={
#                 'clientSecret': str(intent['client_secret'])
#             }, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response(data={"error": str(e)}, status=status.HTTP_403_FORBIDDEN)


# class StripeCheckoutPaymentView(APIView):
#     def post(self, request, *args, **kwargs):
#         try:
#             price = request.data.get('price')
#             user_id = self.request.user.id
#             product_id = request.data.get('product_id')
#             payment_method_id = request.data.get('payment_method_id')

#             print(price, user_id, product_id, payment_method_id)
#             # order = createOrder(price=price, status="PENDING",
#             #             customer_id=user_id, product_id=product_id)
#             # order.save()
#         #     stripe.api_key = f"{settings.STRIPE_SECRET_KEY}"
#         #     payment_intent = stripe.PaymentIntent.create(
#         #         amount=int(4) * 100,
#         #         currency='usd',
#         #         payment_method=payment_method_id,
#         #         confirmation_method='manual',
#         #         confirm=True,
#         #         return_url='http://127.0.0.1:8000/success',
#         #     )

#         #     payment_check = payment_intent['status']
#         #     print("payment_check: ", payment_check)
#         #     order.status = "PAID"
#             return Response(data={"success": True}, status=status.HTTP_200_OK)
#         # except stripe.error.CardError as e:
#         #     print("stripe.error.CardError: ", e.error.message)
#         #     return Response(data={"error": str(e.error.message)}, status=status.HTTP_400_BAD_REQUEST)
#         # except stripe.error.InvalidRequestError as e:
#         #     print("stripe.error.InvalidRequestError", e.error.message)
#         #     return Response(data={"error": str(e.error.message)}, status=status.HTTP_400_BAD_REQUEST)
#         except Exception as e:
#             print(e)
#             return Response(data={"exception": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#         # try:
#         #     # Get the payment token from the client-side
#         #     token = request.data.get('token')
#         #     # Create a charge using the token
#         #     payment = stripe.Charge.create(
#         #         amount=int(4) * 100,  # convert amount to cents
#         #         currency='usd',
#         #         description='Actual payment',
#         #         source=token,
#         #     )
#         #     payment_check = payment['paid']
#         #     print(payment_check)
#         #     return Response(data={"success": True}, status=status.HTTP_200_OK)
#         # except stripe.error.CardError as e:
#         #     # Handle card errors
#         #     print(e.error.message)
#         #     return Response(data={"error": str(e.error.message)}, status=status.HTTP_400_BAD_REQUEST)
#         # except Exception as e:
#         #     print(e)
#         #     return Response(data={"exception": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# class OrderAPIView(APIView):
#     def get(self, request, *args, **kwargs):
#         try:
#             price = int(request.data.get('total_price'))
#             card_name = request.data.get('card_name')
#         except Exception as e:
#             print()

#     # def post(self, request, *args, **kwargs):
#     #     try:
#     #         # price = 1000
#     #         # checkout_session = stripe.checkout.Session.create(
#     #         #     payment_method_types=["card"],
#     #         #     line_items=[
#     #         #         {
#     #         #             "price_data": {
#     #         #                 "currency": "usd",
#     #         #                 "unit_amount": int(price) * 100,
#     #         #                 "product_data": {
#     #         #                     "name": "Test Product Name",
#     #         #                     "description": "Test Product Description",
#     #         #                     # "images": [
#     #         #                     #     f"{settings.BACKEND_DOMAIN}/{price.product.thumbnail}"
#     #         #                     # ],
#     #         #                 },
#     #         #             },
#     #         #             "quantity": 5,
#     #         #         }
#     #         #     ],
#     #         #     metadata={"product_id": 12323423455676},
#     #         #     mode="payment",
#     #         #     success_url=settings.PAYMENT_SUCCESS_URL,
#     #         #     cancel_url=settings.PAYMENT_CANCEL_URL,
#     #         # )
#     #         data= stripe.Token.create(
#     #         card={
#     #             "number": int(str(request.data['card_number']).replace(' ','')),
#     #             "exp_month": int(request.data['expiry_date'].split('/')[0]),
#     #             "exp_year": int(int(request.data['expiry_date'].split('/')[1])),
#     #             "cvc": str(int(request.data['cvv'])),
#     #         })
#     #         card_token = data['id']
#     #         payment = stripe.Charge.create(
#     #             amount= int(4)*100,                  # convert amount to cents
#     #             currency='usd',
#     #             description='Example charge',
#     #             source=card_token,
#     #             )

#     #         payment_check = payment['paid']
#     #         print(payment_check,card_token)
#     #         return Response(data={"url": card_token}, status=status.HTTP_200_OK)
#     #         # return Response(data={"url": checkout_session.url}, status=status.HTTP_200_OK)
#     #     except Exception as e:
#     #         print(e)
#     #         return Response(data={"exception": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#     def post(self, request, *args, **kwargs):
#         try:
#             total_price = int(request.data.get('total_price'))
#             card_name = request.data.get('card_name')
#             payment_method_id = request.data.get('payment_method_id')
#             success_url = "http://localhost:3000/success"  # Specify your success URL
#             cancel_url = "http://localhost:3000/cancel"

#             payment_method = stripe.PaymentMethod.create(
#                 type="card",
#                 card={"token": payment_method_id},
#                 billing_details={
#                     "name": card_name,
#                 },
#             )

#             payment_intent = stripe.PaymentIntent.create(
#                 amount=total_price,
#                 currency='usd',
#                 payment_method=payment_method.id,
#                 confirmation_method='manual',
#                 confirm=True,
#                 return_url=success_url,
#             )
#             if payment_intent.status == 'succeeded':
#                 # Add your logic to handle a successful payment
#                 return Response({"message": "Payment successful"}, status=status.HTTP_200_OK)
#             else:
#                 print(payment_intent.status)
#                 # Handle other payment statuses (e.g., requires_action, requires_payment_method, etc.)
#                 return Response({"error": "Payment failed"}, status=status.HTTP_400_BAD_REQUEST)

#         except stripe.error.CardError as e:
#             # Handle card errors
#             return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

#         except Exception as e:
#             print(e)
#             # Something else happened
#             return Response({"error": "Internal server error", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
#             cancel_url = settings.STRIPE_CANCEL_URL
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

class OrdersAPIView(APIView):

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        if(self.request.user.is_admin and  self.request.user.is_staff and self.request.user.is_active) :
            orders = Order.objects.all()
        elif (self.request.user.is_active and not self.request.user.is_admin and not self.request.user.is_staff):
            orders = Order.objects.filter(customer_id__user = self.request.user)
        pending = orders.filter(status="PENDING").count()
        paid = orders.filter(status="PAID").count()
        failed = orders.filter(status="FAILED").count()
        refunded = orders.filter(status="REFUNDED").count()
        payment_details = {"pending": pending, "paid": paid,
                        "failed": failed, "refunded": refunded}
        serialized_data = OrderSerializer(orders, many=True).data
        return Response(data={"orders": serialized_data, "payment_details": payment_details}, status=status.HTTP_200_OK)
        
        
    def post(self, request, *args, **kwargs):

        pass


def createOrder(price, status, customer_id, product_id):
    order = Order.objects.create(
        price=price, status=status, customer_id=customer_id, product_id=product_id)
    return order


class PayGateway(APIView):
    def post(self, request, *args, **kwargs):
        try:
            print("product_id : ", json.loads(
                request.data['product_id'])[0]['id'])
            print("user.id : ", self.request.user.id)
            amount = request.POST.get('amount')

            customer_id = Customer.objects.get(user=self.request.user)
            product_id = Product.objects.get(
                id=json.loads(request.data['product_id'])[0]['id'])
            product_details = json.loads(request.data['product_id'])
            line_items = []
            for product_info in product_details:
                product = get_object_or_404(Product, id=product_info['id'])
                line_item = {
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': product.name,
                            'images': [product.thumbnail_image.url if product.thumbnail_image else product.image_url],
                        },
                        'unit_amount': int(product.cost * 100),
                    },
                    'quantity': product_info['quantity'],
                }
                line_items.append(line_item)

            order = createOrder(
                price=amount, customer_id=customer_id, product_id=product_id, status="PENDING")
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=line_items,
                mode='payment',
                success_url=request.build_absolute_uri(
                    reverse('orders:success')) + '?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=request.build_absolute_uri(
                    reverse('orders:cancel')),
            )
            order.checkout_session_id = checkout_session['id']
            order.save()
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            print(e)
            return JsonResponse({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)


# @csrf_exempt
def handle_payment_success(request):
    session_id = request.GET.get('session_id')
    order = Order.objects.get(checkout_session_id=session_id)
    order.status = "PAID"
    order.save()
    return redirect("http://localhost:5173/success")
    # return JsonResponse({'message': 'Payment successful'})


def handle_payment_cancel(request):
    return JsonResponse({'message': 'Payment Canceled'})


class ExportOrdersExcel(APIView):
    
    @permission_classes([IsAuthenticated])
    def get(self, request):
        # Get all orders
        if (self.request.user.is_admin):
            orders = Order.objects.all()
        elif (self.request.user.is_active and not self.request.user.is_admin and not self.request.user.is_staff):
        # Prepare data for export
            orders = orders = Order.objects.filter(customer_id__user = self.request.user)
        data = [
            ['ID', 'Checkout Session ID', 'Price', 'Status',
                'Created At', 'Updated At', 'Customer ID', 'Product ID']
        ]
        for order in orders:
            data.append([
                order.id,
                order.checkout_session_id,
                order.price,
                order.status,
                order.created_at,
                order.updated_at,
                order.customer_id.id,
                order.product_id.id
            ])

        excel_file = ExcelResponse(
            data, output_filename='orders.xlsx', )

        return FileResponse(excel_file, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
