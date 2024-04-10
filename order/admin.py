from django.contrib import admin
from .models import Order
# Register your models here.
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id',  'price', 'status', 'created_at',)
    # Optionally, you can customize other settings such as list_filter, search_fields, etc.
    fieldsets = [
        ('Order Information', {'fields': ['id', 'checkout_session_id', 'price', 'status', 'created_at', 'updated_at']}),
        ('Customer and Product', {'fields': ['customer_id', 'product_id']}),
    ]
    readonly_fields = ('id', 'checkout_session_id', 'price', 'status', 'created_at', 'updated_at', 'customer_id', 'product_id')
    # Optionally, you can customize other settings such as list_filter, search_fields, etc.

admin.site.register(Order,OrderAdmin)
# admin.site.register(OrderDetail)
