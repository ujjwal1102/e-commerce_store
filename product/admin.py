from django.contrib import admin
from .models import Product,ProductImages,Variant
# Register your models here.

class ProductImagesAdmin(admin.ModelAdmin):
    list_display = ['product_image_id','product_images']
    

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','category','quantity','thumbnail_image','quantity','cost','created_at']
    

class VariantAdmin(admin.ModelAdmin):    
    list_display = ['product_id','details','cost','quantity']




admin.site.register(Product,ProductAdmin)
admin.site.register(ProductImages,ProductImagesAdmin)
admin.site.register(Variant,VariantAdmin)


