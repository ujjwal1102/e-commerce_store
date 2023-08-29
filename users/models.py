from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User  



# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30,null=True) 
    last_name = models.CharField(max_length=30,null=True)
    phone = models.BigIntegerField()
    state = models.CharField(max_length=30)
    country = models.CharField(max_length=30)
    updated_on =  models.DateTimeField('updated on', default=timezone.now)
    address = models.CharField(max_length=300)

# class ProductCategory(models.Model):
#     category_name = models.CharField(max_length=70,db_column='category_name')
#     parent_id = models.ForeignKey("self",on_delete=models.CASCADE,default=0,blank=True,null=True)
#     created_at = models.DateTimeField('created at', default=timezone.now,null=True)
#     status = models.PositiveSmallIntegerField()
  
class Category(models.Model):
    category_name =  models.CharField(max_length=50,db_column='category_name')
    category_uid = models.CharField(max_length=30,primary_key=True)

class ChildCategory(models.Model):
    child_category_id = models.AutoField(auto_created = True,primary_key = True)
    category_uid = models.ForeignKey(Category,on_delete=models.CASCADE)
    child_category_name = models.CharField(max_length=50,db_column='child_category_name')
    
class GrantChildCategory(models.Model):
    grant_child_category_id = models.AutoField(auto_created = True,primary_key = True)
    child_category_id = models.ForeignKey(ChildCategory,on_delete=models.CASCADE)
    grant_child_category_name = models.CharField(max_length=50,db_column='grant_child_category_name')

class Product(models.Model):
    product_id = models.CharField(max_length=10,primary_key=True)
    name = models.CharField(max_length=150,null=True)
    title = models.CharField(max_length=300,null=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    child_category = models.ForeignKey(ChildCategory,on_delete=models.CASCADE,null=True)
    grant_child_category = models.ForeignKey(GrantChildCategory,on_delete=models.CASCADE,null=True)
    details = models.CharField(max_length=1000)
    brand = models.CharField(max_length=100)
    cost = models.IntegerField(default=None)
    description = models.CharField(max_length=3000)
    product_images= models.FileField(upload_to='media/',default=None)
    add_on = models.DateTimeField('add on', default=timezone.now)

    def __str__(self):
        return self.product_id
    
class ProductImages(models.Model):
    
    product_image_id = models.ForeignKey(Product,on_delete=models.CASCADE)
    product_images= models.FileField(upload_to='media/')

class Wishlist(models.Model):
    id = models.AutoField(auto_created=True,primary_key=True)
    user_id = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    product_id = models.ForeignKey(Product,on_delete=models.CASCADE,null=True)