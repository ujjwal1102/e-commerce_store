from .models import Product
from rest_framework import serializers
from category.models import Category

class ProductSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=500, required=True,allow_blank=False,trim_whitespace=True)
    title = serializers.CharField(max_length=300, required=True,allow_blank=False,trim_whitespace=True)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), required=False)
    description = serializers.CharField(max_length=20000, required=False)
    brand = serializers.CharField(max_length=100, required=True)
    cost = serializers.FloatField(default=None, required=False)
    discount_price = serializers.FloatField(default=None, required=False)
    details = serializers.CharField(max_length=2000,required=False)
    quantity = serializers.IntegerField(required=True)
    brand = serializers.CharField(max_length=100, required=False)
    thumbnail_image = serializers.ImageField(required=True)
    images = serializers.ListField(max_length=10000,child=serializers.DictField(),required=False)
    
    # def to_internal_value(self, data):
    #     # Map incoming keys to the expected keys
    #     mapping = {
    #         'name': 'productName',
    #         'title': 'productTitle',
    #         'category': 'productSelectCategory',
    #         'description':'productDescription',
    #         'quantity':'productQuantity',
    #     }

    #     mapped_data = {mapping.get(key, key): value for key, value in data.items()}

    #     # Call the default to_internal_value implementation
    #     return super().to_internal_value(mapped_data)
    def validate_images(self,value):
        
        print("Value ------ ",value)
        # for img in value:
        #     print("image value : ",img)
        #     print(img)
        
        
        
    
    class Meta:
        model = Product
        fields = '__all__'
    
    # def validate(self, data):
    #     errors = {}

    #     # Validate 'name'
    #     if not data.get('productName'):
    #         errors['productName'] = 'Name is required.'

    #     # Validate 'title'
    #     if not data.get('title'):
    #         errors['title'] = 'Title is required.'

    #     # Validate 'category'
    #     if not data.get('category'):
    #         errors['category'] = 'Category is required.'

    #     # Validate 'details'
    #     if not data.get('details'):
    #         errors['details'] = 'Details is required.'

    #     # Validate 'brand'
    #     if not data.get('brand'):
    #         errors['brand'] = 'Brand is required.'


    #     if errors:
    #         raise serializers.ValidationError(errors)

        # return data
    
    
    def create(self, validated_data):
        # Implement your custom create logic here
        # This method is called when creating a new instance
        return Product.objects.create(**validated_data)