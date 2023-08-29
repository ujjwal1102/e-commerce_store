from django.db import models
from product.models import Product
from django.contrib.auth.models import User  
# Create your models here.

class ProductWishlist(models.Model):
    id = models.AutoField(auto_created=True,primary_key=True,null=False)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,null=True)