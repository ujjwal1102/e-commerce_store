from django.contrib import admin
from .models import Category
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id','category_name','parent_id','created_at','status']
    
admin.site.register(Category,CategoryAdmin)
    

