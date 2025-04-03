from rest_framework import serializers
from apps.accounts.models import User
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from apps.utils.enums import *
# from appss.accounts.utils import Util

class UserRegistrationSerializer(serializers.ModelSerializer):
    # import pdb;pdb.set_trace();
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)

    class Meta:
        model = User
        fields = '__all__' 
        extra_kwargs = {
            'password': {'write_only': True}
        }

    # Validating Password and Confirm Password while Registration
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')

        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password don't match")

        return attrs

    def create(self, validated_data):
        # import pdb;pdb.set_trace();
        # validated_data['is_active'] = True
        return User.objects.create_user(**validated_data)
    
    def update(self, instance, validated_data):
        # Ensure is_active is set to True during user update
        validated_data['is_active'] = True
        return super().update(instance, validated_data)


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, required=False)
    username = serializers.CharField(max_length=80, required=False)  # Add this line

    class Meta:
        model = User
        fields = '__all__' # Include 'username' in fields

    def validate(self, attrs):
        email = attrs.get('email')
        username = attrs.get('username')
        

        # Validate that either email or username is provided
        if not email and not username:
            raise serializers.ValidationError("Please provide either email or username.")

        return attrs


class UserProfileSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = '__all__'

