from django.contrib.auth import authenticate, login,  update_session_auth_hash, logout
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from .serializers import UserSerializer, UserRegisterSerializer
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .serializers import UserSerializer, UserLoginSerializer, CustomerSerializer
from users.models import Customer

# # Create your views here.
# class IndexView(viewsets):
#     def retrive(self,*args,**kwargs):
#         pass


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    

    @classmethod
    def get_token(cls, user):
        token = AccessToken.for_user(user)
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        # token['username'] = user.username
        token['is_superuser'] = user.is_admin_user
        token['is_staff'] = user.is_staff_user
        token['is_active'] = user.is_active
        return token


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# from django.middleware import csrf


class RegisterAPIView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        data = request.data
        print("outer : ",request.user)
        print(data)
        serializer = UserRegisterSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            user_data = {"is_staff": user.is_staff_user,
                         "is_admin": user.is_admin_user, "is_active": user.is_active}
            print(user)
            login(request, user)
            token_serializer = CustomTokenObtainPairSerializer()
            token = token_serializer.get_token(user)
            response_data = {
                    'user': serializer.data,
                    'token': {
                        'refresh': str(token),
                        'access': str(token),
                    },
                    # 'session_id': session_id,
                    'user_data': user_data,
                }
            print('user created')
            return Response(data={'data': response_data, }, status=status.HTTP_200_OK)
        else:
            # print(serializer.errors)
            # print(serializer.error_messages)
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        # else:
        #     return Response(serializer.errors, status=status.HTTP_200_OK)


class LoginAPIView(APIView):
    permission_classes = (permissions.AllowAny,)
    # authentication_classes = (SessionAuthentication,)

    def post(self, request):
        data = request.data

        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            user, user_data = serializer.check_user(data)
            if user is not None:
                login(request, user)
                session_id = request.session.session_key

                # token = get_tokens_for_user(user)
                token_serializer = CustomTokenObtainPairSerializer()
                token = token_serializer.get_token(user)

                response_data = {
                    'user': serializer.data,
                    'token': {
                        'refresh': str(token),
                        'access': str(token),
                    },
                    'session_id': session_id,
                    'user_data': user_data,
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    # def post(self, request):
    #     username = request.data.get('username')
    #     password = request.data.get('password')
    #     user = authenticate(request, username=username, password=password)

    #     if user:
    #         login(request, user)
    #         return Response(UserSerializer(user).data)
    #     else:
    #         return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)


class UserView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    # authentication_classes = (SessionAuthentication,)

    def get(self, request, format=None):
        # print(request.user)
        # print(permissions.IsAuthenticated)
        serializer = UserSerializer(request.user)
        print(serializer)
        return Response({'user': serializer.data}, status=status.HTTP_200_OK)


class CustomerView(APIView):
    def get(self, request, format=None):
        print(self.request.user.id)
        customer = get_object_or_404(Customer, user=self.request.user.id)
        print(customer)
        if customer:
            customer = CustomerSerializer(customer).data
            print(customer)
        return Response(data={"customer": customer}, status=status.HTTP_200_OK)

    def post(self, request, format=None): 
    
        customer = get_object_or_404(Customer, user=self.request.user.id)
        if customer:
            serializer = CustomerSerializer(customer, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(data={"customer": serializer.data,"message": "Profile updated successfully"}, status=status.HTTP_200_OK)
            else:
                return Response(data={"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data={"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
    def put(self, request, format=None): pass
    def delete(self, request, format=None): pass
