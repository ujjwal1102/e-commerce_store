from category.models import Category
from rest_framework import serializers
# from django.core.exceptions import ValidationError


class CategorySerializer(serializers.ModelSerializer):

    categories = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = '__all__'

    # def get_categories(self, obj):
    #     print(obj.category_name)
    #     children_qs = Category.objects.filter(parent_id=obj)
    #     children_serializer = CategorySerializer(children_qs, many=True)
    #     return children_serializer.data
    # def get_categories(self, obj):
    #     children_qs = Category.objects.filter(parent_id=obj.id)
    #     if children_qs.exists():
    #         children_serializer = CategorySerializer(children_qs, many=True)
    #         return children_serializer.data
    #     return None
    def get_categories(self, obj):
        children_qs = Category.objects.filter(parent_id=obj.id)
        children_serializer = CategorySerializer(children_qs, many=True)
        children_data = children_serializer.data

        # Exclude categories with no children
        if children_data:
            return children_data
        return None


class CategoryFormSerializer(serializers.ModelSerializer):

    categories = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = '__all__'
    def get_categories(self, obj):
        children_qs = Category.objects.filter(parent_id=obj.id)
        children_serializer = CategorySerializer(children_qs, many=True)
        children_data = children_serializer.data

        if children_data:
            return children_data
        return None
