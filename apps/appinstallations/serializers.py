from rest_framework import serializers
from .models import AppInstallation

class AppInstallationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = AppInstallation
        fields = '__all__' 

