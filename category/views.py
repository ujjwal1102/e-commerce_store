from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from category.serializers import CategorySerializer
from category.models import Category
from django.db.models import Q, Subquery


class CategoryView(APIView):
    def get(self, *args, **kwargs):
        
        categories = Category.objects.filter(Q(parent_id__isnull=True) | Q(
            parent_id__in=Category.objects.filter(parent_id__isnull=True).values_list("id", flat=True))).all()
        print(categories)
        serializer = CategorySerializer(categories, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        data = request.data
        serializer = CategorySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

        else:

            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

