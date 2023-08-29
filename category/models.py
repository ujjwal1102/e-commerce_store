from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User  


# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=70,db_column='category_name')
    parent_id = models.ForeignKey("self",on_delete=models.CASCADE,default="Parent Category",blank=True,null=True)
    created_at = models.DateTimeField('created at', default=timezone.now,null=True)
    status = models.PositiveSmallIntegerField(default=1)
    
    # def __str__(self) -> str:
    #     super().__str__()
    #     return self.category_name
    
    
