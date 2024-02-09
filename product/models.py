from django.db import models
from category.models import Category
from django.utils import timezone
from django.urls import reverse


class Brand(models.Model):
    id = models.AutoField(auto_created=True,primary_key=True,null=False)
    brand_name = models.CharField(max_length=150,null=False)
    
    def __str__(self) -> str:
        return self.brand_name
    
class Product(models.Model):
    id = models.AutoField(auto_created=True,primary_key=True,null=False)
    name = models.CharField(max_length=500,null=True)
    title = models.CharField(max_length=300,null=True)
    category = models.ForeignKey(Category,on_delete=models.PROTECT,null=True)
    details = models.TextField(max_length=2000,null=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True, blank=True)
    cost = models.FloatField(default=None,null=True)
    description = models.TextField(max_length=5000,editable=True,null=True)
    quantity = models.PositiveIntegerField(null=True)
    features = models.JSONField(default=None,null=True)
    thumbnail_image = models.ImageField(upload_to='media/thumbnail',default=None,null=True)
    created_at = models.DateTimeField('created_at', default=timezone.now,)
    image_url = models.URLField(max_length = 200,null=True) 
    discount_price = models.FloatField(default=None, null=True)
    
    
    def get_absolute_url(self):
        return reverse('prod_detail', args=[str(self.id)])
    
    def filter_products_data(self,filter_data={}):
        new_data = None
        if filter_data:
            filter_keys = filter_data.keys()
            
            for k in filter_keys:
                new_data = self.objects.filter(k = k)
            
        
        return
    # def get_the_fields

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
    
    
class ProductUtils(models.Model):
    id = models.AutoField(auto_created=True,primary_key=True,null=False)
    product_id = models.ForeignKey(Product,on_delete=models.CASCADE)
    visit_count = models.PositiveBigIntegerField(default=None, null=True)
