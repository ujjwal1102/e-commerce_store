from django.contrib import admin
from .models import Product,ProductImages,Variant,Brand,ProductUtils,ProductReview
# Register your models here.

class ProductImagesAdmin(admin.ModelAdmin):
    list_display = ['product_image_id','product_images']
    

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','category','quantity','thumbnail_image','quantity','cost','created_at']
    

class VariantAdmin(admin.ModelAdmin):    
    list_display = ['product_id','details','cost','quantity']

class BrandAdmin(admin.ModelAdmin):
    list_display = ['brand_name']

class ProductReviewAdmin(admin.ModelAdmin):
    empty_value_display = "-empty-"
    fields = [( "user","product"),"rating","review"]
    

admin.site.register(Product,ProductAdmin)
admin.site.register(ProductImages,ProductImagesAdmin)
admin.site.register(Variant,VariantAdmin)
admin.site.register(Brand,BrandAdmin)
admin.site.register(ProductUtils)
admin.site.register(ProductReview, ProductReviewAdmin)