from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from category.serializers import CategorySerializer,CategoryFormSerializer
from category.models import Category
from django.db.models import Q, Subquery


class CategoryView(APIView):
    def get(self, *args, **kwargs):

        categories = Category.objects.filter(Q(parent_id__isnull=True) | Q(
            parent_id__in=Category.objects.filter(parent_id__isnull=True).values_list("id", flat=True))).all()
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

class CategoryFormView(APIView):
    def get(self, *args, **kwargs):
        categories = Category.objects.all()
        serializer = CategoryFormSerializer(categories, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

class SelectCategoryView(APIView):
    def post(self, request, format=None):
        try:
            p_id = request.data['id']
            if p_id is not None or p_id != {}:
                categories = Category.objects.exclude(parent_id__isnull=True).filter(
                    Q(parent_id=p_id)).all()
                print(categories.count())
                serializer = CategorySerializer(categories, many=True)
                return Response(data={"data": serializer.data, "has_child": categories.count()}, status=status.HTTP_201_CREATED)
            else:
                return Response(data='requires `id` ', status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response(data=str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
