
from rest_framework.views import APIView
from wishlist.models import ProductWishlist
from wishlist.serializers import WishlistSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from users.models import User
from product.models import Product

class WishlistAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self,request):
        # user_id = request.user.id
        print(type(request.data))
        print(request.user.id)
        user = get_object_or_404(User,id=request.user.id)
        wishlist = ProductWishlist.objects.filter(user=user)
        serializer = WishlistSerializer(wishlist,many=True)
        print("data : ",serializer.data)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    def post(self,request,format=None):
        data = request.data
        
        print("data : ",data,request.user)
        print(request.user.id)
        user = get_object_or_404(User,id=request.user.id)
        product = get_object_or_404(Product,id=data['product'])
        serializer = WishlistSerializer(data={'user':user.id,'product':product.id})
        # print(serializer)
        if serializer.is_valid():
            # print(serializer)
            wishlist = serializer.save()
            print(wishlist)
            data = WishlistSerializer(wishlist).data
            return Response(data=data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(data={'errors':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request, pk):
        try:
            instance = ProductWishlist.objects.get(pk=pk)
        except ProductWishlist.DoesNotExist:
            return Response({"error": "Object not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = WishlistSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request):
        print(request.user.id,request.data)
        try:
            instance = ProductWishlist.objects.get(user=request.user,product__id=request.data.get("id"))
        except ProductWishlist.DoesNotExist:
            return Response({"error": "Object not found"}, status=status.HTTP_404_NOT_FOUND)
        
        print(instance)
        instance.delete()
        return Response({"message": "Object deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    
