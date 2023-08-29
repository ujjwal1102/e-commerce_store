from django.contrib import admin
from .models import Product,Category,Customer,ProductImages,Wishlist,ChildCategory,GrantChildCategory
# Register your models here.

class ProductImagesAdmin(admin.ModelAdmin):
    list_display = ['product_image_id','product_images']

class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_id','name','title','category','product_images','cost','add_on']

admin.site.register(Product,ProductAdmin)
admin.site.register(Customer)
admin.site.register(Category)
admin.site.register(ProductImages,ProductImagesAdmin)
admin.site.register(Wishlist)
admin.site.register(ChildCategory)
admin.site.register(GrantChildCategory)

