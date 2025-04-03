
from rest_framework import serializers
from .models import *

class CustomerusersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customerusers
        fields = '__all__' 