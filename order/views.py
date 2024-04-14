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

stripe.api_key = settings.STRIPE_SECRET_KEY


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


def handle_payment_cancel(request):
    return JsonResponse({'message': 'Payment Canceled'})


class ExportOrdersExcel(APIView):
    
    @permission_classes([IsAuthenticated])
    def get(self, request):
        # Get all orders
        if (self.request.user.is_admin):
            orders = Order.objects.all()
        elif (self.request.user.is_active and not self.request.user.is_admin and not self.request.user.is_staff):
        
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
