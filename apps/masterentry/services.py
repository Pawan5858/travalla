# python builtins
import logging
import logging.config
import random
import string
# from num2words import num2words
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from django.db import transaction
from apps.utils.enums import ResStatus
from django.db.models import Q
from apps.utils.utility import *
from datetime import datetime
from django.db.models.functions import Concat
from django.utils.timezone import make_aware
from django.db.models import Sum, F, Subquery, OuterRef, DecimalField, Max, Count
from django.shortcuts import get_object_or_404
from django.db.models.functions import TruncDate
from django.db.models import Q
import threading
from django.db.models import Q, Case, When, IntegerField
from django.db import connection
from decimal import Decimal
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.http import HttpResponse
from .serializers import *
from django.db.models import Count, OuterRef, Subquery
from django.db.models.functions import Coalesce
from django.core.paginator import Paginator
from django.db.models import Prefetch
logger = logging.getLogger(__name__)


class masterEntryServices(object):
    def __init__(self):
        self.utility = Utility()
        self.log =logging.getLogger(__name__)
    
    def get_languages(self):
        try:
            languages = Languages.objects.all()
            serializer=LanguagesSerializer(languages, many=True)
            

            return Response({
                'messages': "Get languages successfully.",  # Fixed typo here
                'data': serializer.data,
                'status': ResStatus.success.value
            }, status=status.HTTP_200_OK)

        except Exception as err:
            self.log.error(f"Error fetching languages: {err}")
            return Response(
                {
                    "status": ResStatus.error.value,
                    "message": "Unable to get languages.",
                    "errorDetails": str(err)
                },status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    def get_skills(self):
        try:
            skills = Skills.objects.all()
            serializer=SkillsSerializer(skills, many=True)
            

            return Response({
                'messages': "Get skills successfully.",  # Fixed typo here
                'data': serializer.data,
                'status': ResStatus.success.value
            }, status=status.HTTP_200_OK)

        except Exception as err:
            self.log.error(f"Error fetching skills: {err}")
            return Response(
                {
                    "status": ResStatus.error.value,
                    "message": "Unable to get skills.",
                    "errorDetails": str(err)
                },status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            
    def get_document_types(self):
        try:
            
            documentstypes = DocumentTypes.objects.all()
            serializer=DocumentTypesSerializer(documentstypes, many=True)
            

            return Response({
                'messages': "Get documents types successfully.",  # Fixed typo here
                'data': serializer.data,
                'status': ResStatus.success.value
            }, status=status.HTTP_200_OK)

        except Exception as err:
            self.log.error(f"Error fetching documents types: {err}")
            return Response(
                {
                    "status": ResStatus.error.value,
                    "message": "Unable to get documents types.",
                    "errorDetails": str(err)
                },status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            
    def get_guide_types(self):
        try:
            guidetypes = GuideTypes.objects.all()
            serializer=GuideTypesSerializer(guidetypes, many=True)
            

            return Response({
                'messages': "Get documents types successfully.",  # Fixed typo here
                'data': serializer.data,
                'status': ResStatus.success.value
            }, status=status.HTTP_200_OK)

        except Exception as err:
            self.log.error(f"Error fetching documents types: {err}")
            return Response(
                {
                    "status": ResStatus.error.value,
                    "message": "Unable to get documents types.",
                    "errorDetails": str(err)
                },status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
    
