from rest_framework import serializers
from .models import *

class LanguagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Languages
        fields = '__all__'
        
        
class SkillsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skills
        fields = '__all__'
        
class DocumentTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentTypes
        fields = '__all__'
        
class GuideTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuideTypes
        fields = '__all__'