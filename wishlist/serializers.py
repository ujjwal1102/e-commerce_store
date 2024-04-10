from rest_framework import serializers
from wishlist.models import ProductWishlist
from users.serializers import UserSerializer
from product.serializers import ProductSerializer
from product.models import Product
from users.models import User


class WishlistSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = ProductWishlist
        fields = ['user', 'product']
        depth = 1


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        user_data = UserSerializer(instance.user).data
        product_data = ProductSerializer(instance.product).data
        representation.update({'user': user_data.get('id'), 'product': {'id':product_data.get('id'),'title': product_data.get(
            'title'), 'name': product_data.get('name'), 'cost': product_data.get('cost'),'thumbnail_image': product_data.get('thumbnail_image'),'image_url':product_data.get('image_url') }})
        return representation
