from django.shortcuts import render
from apps.utils.enums import *
from django.shortcuts import redirect
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.utils.utility import *
from apps.utils.session_handler import *
import logging
import logging.config
from .services import *
from collections import OrderedDict
from .models import *
from .serializers import *

logger = logging.getLogger(__name__)

class masterEntryAPIViewContoller(APIView):
    
    def __init__(self):
        self.service = masterEntryServices()
        self.utility = Utility()
        self.sessionHandler =SessionHandler()
        self.log =logging.getLogger(__name__)
        
    def get(self, request, api_version=None , subRoute=None, subdomain =None):
        if subRoute == 'languages':  # New subroute
            return self.service.get_languages()
        elif subRoute == 'skills': 
            return self.service.get_skills()
        
        elif subRoute == 'document_types': 
            return self.service.get_document_types()
        
        elif subRoute == 'guide_types': 
            return self.service.get_guide_types()
        else:
            return Response({'status': ResStatus.error.value, 'message': 'GET CALL'}, 
                            status=status.HTTP_400_BAD_REQUEST)
            
            
    
    def post(self, request, subRoute):
        try:
            pass    
        except Exception as err:

            logger.error('masterEntry Contoller exception: Required fields are empty: %s', str(err), exc_info=True)

            return Response({'status': ResStatus.error.value, 'message': 'masterEntry Contoller error ' + str(err)}, 
                            status=status.HTTP_400_BAD_REQUEST)
            
    def put(self, request, subRoute):
        try:
           pass
        except Exception as err:

            logger.error('ordersr updateRazorpayPayment exception: Required fields are empty: %s', str(err), exc_info=True)

            return Response({'status': ResStatus.error.value, 'message': 'Payment failed with error ' + str(err)}, 
                            status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, subRoute):
        try:
            pass
        except Exception as err:
            logger.error('ordersr updateRazorpayPayment exception: Required fields are empty: %s', 
                        str(err), exc_info=True)

            return Response({'status': ResStatus.error.value, 
                            'message': 'Payment failed with error ' + str(err)}, 
                            status=status.HTTP_400_BAD_REQUEST) 
            
    # def fileTypes(self):
    #     try:
            
    #         types = FileTypes.objects.all()
    #         serializer = FileTypesSerializer(types, many=True)
    #         return serializer.data
                
    #     except Exception as err:
    #         self.log.error('Error in masterentry service unable get FileTypes : %s', str(err), exc_info=True)
    #         return Response({'status': ResStatus.error.value,
    #                         'message': 'Unable to retrieve FileTypes.',
    #                         'devMsg': str(err)}, status=status.HTTP_400_BAD_REQUEST)  
            
    
