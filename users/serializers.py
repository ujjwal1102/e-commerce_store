from users.models import User, Customer
from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model, authenticate
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.db import transaction
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        if not User.objects.filter(email=attrs['email']).exists():
            raise ValidationError({'username': 'This email does not exist.'})

        # Check if the password is too short.
        if len(attrs['password']) < 8:
            raise ValidationError(
                {'password': 'Your password must be at least 8 characters long.'})

        return attrs

    def check_user(self, clean_data):
        user = authenticate(
            username=clean_data['email'], password=clean_data['password'])
        if user is not None:
            user_data = User.objects.get(email=clean_data['email'])
            # print("user_data.is_staff : ",user_data.is_staff_user,"user_data.is_admin : ",user_data.is_admin_user,"user_data.is_active : ",user_data.is_active)
            user_data = {"is_staff": user_data.is_staff_user,
                         "is_admin": user_data.is_admin_user,
                         "is_active": user_data.is_active,
                         "is_seller": user.is_seller_user,
                         "is_customer": user.is_customer_user}
            if not user:
                raise ValidationError('user not found')
            return user, user_data
        else:
            return (None, "Email or password is Incorrect")


class UserRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all(),
                                    message="Email already exists...!")]
    )

    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password], error_messages={
            'blank': 'Password should not be blank.'
        })
    confirm_password = serializers.CharField(write_only=True, required=True, error_messages={
        'blank': 'Confirm Password should not be blank.'
    })

    class Meta:
        model = User
        fields = ('password', 'confirm_password',
                  'email', )

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password', None)
        user_type = self.context.get('user_type', None)
        with transaction.atomic():
            if user_type == 'customer':
                user = User.objects.create_customer(**validated_data)
            elif user_type == 'seller':
                user = User.objects.create_seller(**validated_data)
            else:
                user = super().create(validated_data)

        user.set_password(validated_data['password'])
        user.save()

        return user


class CustomerSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    first_name = serializers.CharField(max_length=30, allow_null=True, required=False)
    last_name = serializers.CharField(max_length=30, allow_null=True, required=False)
    phone = serializers.CharField(required=False)
    address = serializers.CharField(max_length=800, allow_blank=True, required=False)
    country = serializers.CharField(max_length=200, allow_blank=True, required=False)
    state = serializers.CharField(max_length=30, allow_blank=True, required=False)
    city = serializers.CharField(max_length=30, allow_blank=True, allow_null=True, required=False)
    pin_code = serializers.CharField(max_length=6, allow_blank=True, allow_null=True, required=False)

    class Meta:
        model = Customer
        fields = '__all__'
        depth = 2

    def validate_phone(self, value):
        """
        Validate that the phone number is a valid integer.
        """
        if value and not value.isdigit():
            raise serializers.ValidationError("Phone number must contain only digits.")
        
        return value

    def validate(self, data):
        """
        Validate the serializer data.
        """
        return data
    
    
