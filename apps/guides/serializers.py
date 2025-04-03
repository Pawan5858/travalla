
from rest_framework import serializers
from .models import *
from apps.masterentry.serializers import *

class GuideLanguagesSerializer(serializers.ModelSerializer):
    gdln_lang = LanguagesSerializer(read_only=True, source='gdln_lang')
    class Meta:
        model = GuideLanguages
        fields = '__all__'
        
        
        
class GuideSkillsSerializer(serializers.ModelSerializer):
    gdsk_skil =SkillsSerializer(read_only=True, source='gdsk_skil')
    class Meta:
        model = GuideSkills
        fields = '__all__'
        
class GuideDocumentsSerializer(serializers.ModelSerializer):
    gddc_doct = DocumentTypesSerializer(read_only=True, source='gddc_doct')
    class Meta:
        model = GuideDocuments
        fields = '__all__'
        

class GuidesSerializer(serializers.ModelSerializer):
    language = GuideLanguagesSerializer(many=True,read_only=True,source='guidelanguages_set')
    skills = GuideSkillsSerializer(many=True,read_only=True,source='guideskills_set')
    documents = GuideDocumentsSerializer(many=True,read_only=True,source='guidedocuments_set')
    gude_type = GuideTypesSerializer(read_only=True, source='gude_type')
    class Meta:
        model = Guides
        fields = '__all__'
        