from .models import Product, Brand

from rest_framework import serializers
from category.models import Category
from django.core.validators import MinLengthValidator
from users.models import User


class ProductSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        max_length=500, required=True, allow_blank=False, trim_whitespace=True, validators=[
            MinLengthValidator(
                limit_value=1, message='It should not be empty.')
        ], error_messages={
            'blank': 'Name should not be blank.'
        })
    title = serializers.CharField(
        max_length=300, required=True, allow_blank=False, trim_whitespace=True, error_messages={
            'blank': 'Title should not be blank.'
        })
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), required=False, error_messages={
            'incorrect_type': 'Select a category.'
        })
    description = serializers.CharField(max_length=20000, required=False, error_messages={
        'blank': 'Title should not be blank.'
    })
    brand = serializers.CharField(max_length=100, required=True, error_messages={
        'blank': 'Title should not be blank.'
    })
    cost = serializers.FloatField(default=None, required=False, error_messages={
        'blank': 'Title should not be blank.'
    })
    discount_price = serializers.FloatField(default=None, required=False,)
    details = serializers.CharField(max_length=2000, required=False)
    quantity = serializers.IntegerField(required=True, error_messages={
        'blank': 'Quantity should not be blank.', 'invalid': 'Set the quantity',
    })
    brand = serializers.CharField(max_length=100, required=False, error_messages={
        'blank': 'Brand should not be blank.'
    })
    thumbnail_image = serializers.ImageField(required=True, error_messages={
        'blank': 'Thumbnail Image should not be blank.'
    })
    images = serializers.ListField(
        max_length=10000, child=serializers.DictField(), required=False)
    seller = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False, error_messages={
        'incorrect_type': 'Set the seller.'
    })

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

    def validate_images(self, value):

        print("Value ------ ", value)
        for img in value:
            print("image value : ", img)
            print(img)

    class Meta:
        model = Product
        fields = '__all__'

    def validate_name(self, name):
        # print("validate_name(self,name) : ", name)
        if name is None or '':
            raise serializers.ValidationError('Name Should not be empty')
        return name

    # def validate(self, data):
    #     print("validate(self, data): ",data)
    #     errors = {}

    #     # Custom validation for name
    #     name = data.get('name', '')
    #     if not name.strip():
    #         errors['name'] = 'Name should not be blank.'

    #     # Custom validation for quantity
    #     quantity = data.get('quantity')
    #     if quantity is not None and quantity <= 0:
    #         errors['quantity'] = 'Quantity must be a positive integer.'

    #     # Custom validation for thumbnail_image
    #     thumbnail_image = data.get('thumbnail_image')
    #     if thumbnail_image and not isinstance(thumbnail_image, (bytes, bytearray)):
    #         errors['thumbnail_image'] = 'Invalid file format. Must be a valid image file.'

    #     if errors:
    #         raise serializers.ValidationError(errors)

    #     return data

    def create(self, validated):
        # Implement your custom create logic here
        # This method is called when creating a new instance
        return Product.objects.create(**validated)


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'
