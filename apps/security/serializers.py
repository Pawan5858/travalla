from rest_framework import serializers
from .models import *
from apps.accounts.models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'