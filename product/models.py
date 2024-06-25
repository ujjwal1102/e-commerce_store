from django.db import models
from category.models import Category
from django.utils import timezone
from django.urls import reverse
from users.models import User
from django.db.models import Q,Count

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
    seller = models.ForeignKey(User,on_delete=models.CASCADE,null=True, blank=True)
    
    
    def get_absolute_url(self):
        return reverse('prod_detail', args=[str(self.id)])
    
    @classmethod
    def filter_products(cls,filter_data):
        """
        Filter products based on filter_data dictionary.
        filter_data: Dictionary containing filtering criteria.
        
        Example: {'category__name__icontains': 'electronics', 'brand__name__icontains': 'sony'}
        """
        query = Q()
        for key, value in filter_data.items():
            query &= Q(**{key: value})
        
        products = cls.objects.filter(query)
        
        # Get unique categories with their count
        categories = products.values('category__category_name').annotate(count=Count('category')).order_by('category__category_name')

        # Get unique brands with their count
        brands = products.values('brand__brand_name').annotate(count=Count('brand')).order_by('brand__brand_name')
        # print(categories, brands)
        return products
        
         
    @classmethod
    def filter_by_name(cls,name):
        return cls.objects.filter(name__icontains=name)

    # @classmethod
    # def filter_by_title(cls,title):
    #     return cls.objects.filter(title__icontains=title)
    
    # @classmethod
    # def filter_by_brand(cls,brand):
    #     return cls.objects.filter(brand__icontains=brand)
    
    # @classmethod
    # def filter_by_name(cls,name):
    #     return cls.objects.filter(name__icontains=name)
    
    # @classmethod
    # def filter_by_name(cls,name):
    #     return cls.objects.filter(name__icontains=name)
    
    # @classmethod
    # def filter_by_name(cls,name):
    #     return cls.objects.filter(name__icontains=name)
        

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
