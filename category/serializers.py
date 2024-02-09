from category.models import Category
from rest_framework import serializers
# from django.core.exceptions import ValidationError



class CategorySerializer(serializers.ModelSerializer):

    # categories = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = '__all__'     
        
    # def get_categories(self, obj):
    #     print(obj.category_name)
    #     children_qs = Category.objects.filter(parent_id=obj)
    #     children_serializer = CategorySerializer(children_qs, many=True)
    #     return children_serializer.data