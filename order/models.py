from django.db import models
from users.models import Customer
from product.models import Product
# Create your models here.

class Order(models.Model):
    id = models.AutoField(auto_created=True,primary_key=True,null=False)
    # order_id = models.CharField(default=f'ODR-{id}', editable=False)
    price = models.BigIntegerField(null=True)
    status = models.BooleanField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    
class OrderDetail(models.Model):
    id = models.AutoField(auto_created=True,primary_key=True,null=False)
    order_id = models.ForeignKey(Order,on_delete=models.CASCADE)
    customer_id = models.ForeignKey(Customer,on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product,on_delete=models.CASCADE)