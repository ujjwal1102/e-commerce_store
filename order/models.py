from django.db import models
from users.models import Customer
from product.models import Product
# Create your models here.


class Order(models.Model):

    id = models.AutoField(auto_created=True, primary_key=True, null=False)
    checkout_session_id = models.CharField(
        max_length=200, editable=False, null=True)
    price = models.BigIntegerField(null=True)
    status = models.CharField(max_length=200, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    customer_id = models.ForeignKey(
        Customer, on_delete=models.CASCADE, )
    product_id = models.ForeignKey(
        Product, on_delete=models.CASCADE, )


# class OrderDetail(models.Model):
#     id = models.AutoField(auto_created=True,primary_key=True,null=False)
#     order_id = models.ForeignKey(Order,on_delete=models.CASCADE)
#     customer_id = models.ForeignKey(Customer,on_delete=models.CASCADE)
#     product_id = models.ForeignKey(Product,on_delete=models.CASCADE)
