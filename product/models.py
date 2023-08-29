from django.db import models
from category.models import Category
from django.utils import timezone
from django.urls import reverse
# Create your models here.


class Product(models.Model):
    id = models.AutoField(auto_created=True,primary_key=True,null=False)
    name = models.CharField(max_length=150,null=True)
    title = models.CharField(max_length=300,null=True)
    category = models.ForeignKey(Category,on_delete=models.PROTECT)
    details = models.TextField(max_length=2000)
    brand = models.CharField(max_length=100)
    cost = models.IntegerField(default=None)
    description = models.TextField(max_length=5000,editable=True)
    quantity = models.PositiveIntegerField()
    thumbnail_image = models.ImageField(upload_to='media/thumbnail',default=None)
    created_at = models.DateTimeField('created_at', default=timezone.now)
    
    def get_absolute_url(self):
        return reverse('prod_detail', args=[str(self.id)])


class Variant(models.Model):
    id = models.AutoField(auto_created=True,primary_key=True,null=False)
    product_id = models.ForeignKey(Product,on_delete=models.CASCADE)
    details = models.TextField(max_length=2000)
    cost = models.IntegerField(default=None)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField('created_at', default=timezone.now)
    
class ProductImages(models.Model):
    id = models.AutoField(auto_created=True,primary_key=True,null=False)
    product_image_id = models.ForeignKey(Product,on_delete=models.CASCADE)
    product_images = models.FileField(upload_to='media/')
    created_at = models.DateTimeField('created_at', default=timezone.now)