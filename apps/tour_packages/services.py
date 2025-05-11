# python builtins
import logging
import logging.config
# from num2words import num2words
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from django.db import transaction
from apps.utils.enums import ResStatus
from apps.utils.utility import *
from datetime import datetime
from .serializers import *
logger = logging.getLogger(__name__)
from .models import *
import random
import string
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import datetime, timedelta

from django.utils import timezone


class tourPackagesServices(object):
    def __init__(self):
        self.utility = Utility()
        self.log =logging.getLogger(__name__)
        
    @transaction.atomic
    def add_tour_package(self, request):
        try:
            # import pdb;
            # pdb.set_trace()
            
            payload =request.data
            image =request.FILES.get('image')
            
            if image:
                if image.name == '':
                    transaction.set_rollback(True)
                    return {'status': 'error', 'message': 'Please add a valid image file.'}
                image_filename = Utility().generateSecureFileNameAndSave('travellers_images' , image)
            
            package_data = {
                'torp_name': payload.get('name'),
                'torp_package_type': payload.get('packagetype'),
                'torp_price': payload.get('price'),
                'torp_duration': payload.get('duration'),
                'torp_description': payload.get('description'),
                'torp_inclusions': payload.get('inclusions'),
                'torp_start_date': payload.get('start_date'),  # Fixed typo and matched model field
                'torp_end_date': payload.get('end_date'),      # Matched model field
                'torp_destination': Destination.objects.get(dest_id=payload.get('pdestination')),
                'torp_start_location': Destination.objects.get(dest_id=payload.get('pstatelocation')),
                'torp_end_destination': Destination.objects.get(dest_id=payload.get('penddestination')),
                'torp_inclusions':payload.get('inclusion'),
                'torp_image' :'media/travellers_images/'+image_filename
            }

            # Create and save tour package
            package = TourPackage(**package_data)
            package.save()

            # Handle Itineraries for ITINERARY package
            if package.torp_package_type == 'ITINERARY':
                itinerary_data = json.loads(payload.get('Itinerary'))
                if not itinerary_data:
                    return Response({
                        'status': 'error',
                        'message': 'Itinerary data required for ITINERARY package type'
                    }, status=status.HTTP_400_BAD_REQUEST)
                
        
                for index, obj in enumerate(itinerary_data, 1):
                    itinerary = TourPackageItinerary(
                                itnr_package=package,
                                itnr_day_number=index,
                                itnr_date=obj['date'],
                                itnr_activities=obj['desc'],
                                itnr_location=obj['loc']
                            )
                    itinerary.save()
            
            return Response({
                'status': 'success',
                'message': 'Tour package added successfully.',
                'package_id': package.torp_id
            }, status=status.HTTP_201_CREATED)

        
        except Exception as err:
            transaction.set_rollback(True)
            self.log.error(f"Error creating tour package: {str(err)}")
            return Response({
                'status': 'error',
                'message': 'Unable to add tour package. Please try again.',
                'devMsg': str(err)
            }, status=status.HTTP_400_BAD_REQUEST)    
        
    @transaction.atomic
    def update_tour_package(self, payload):
        try:
            
            package = TourPackage.objects.get(torp_id =payload.get('id'))
            
            # update values
            package.torp_name=payload.get('name')
            package.torp_package_type =payload.get('packagetype')
            package.torp_price = payload.get('price')
            package.torp_duration= payload.get('duration')
            package.torp_description =payload.get('description')
            package.torp_inclusions= payload.get('inclusions')
            package.torp_start_date= payload.get('start_date')
            package.torp_end_date=payload.get('end_date')
            package.torp_destination=Destination.objects.get(dest_id=payload.get('pdestination'))
            package.torp_start_location=Destination.objects.get(dest_id=payload.get('pstatelocation'))
            package.torp_end_destination =Destination.objects.get(dest_id=payload.get('penddestination'))
        
            package.save()

            # Handle Itineraries for ITINERARY package
            if payload.get('packagetype') == 'ITINERARY':
                TourPackageItinerary.objects.filter(itnr_package=package).delete()
                
                itinerary_data = json.loads(payload.get('Itinerary'))
                if not itinerary_data:
                    return Response({
                        'status': 'error',
                        'message': 'Itinerary data required for ITINERARY package type'
                    }, status=status.HTTP_400_BAD_REQUEST)
                
        
                for index, obj in enumerate(itinerary_data, 1):
                    itinerary = TourPackageItinerary(
                                itnr_package=package,
                                itnr_day_number=index,
                                itnr_date=obj['date'],
                                itnr_activities=obj['desc'],
                                itnr_location=obj['loc']
                            )
                    itinerary.save()
            
            return Response({
                'status': 'success',
                'message': 'Tour package update successfully.',
                'package_id': package.torp_id
            }, status=status.HTTP_201_CREATED)

        
        except Exception as err:
            transaction.set_rollback(True)
            self.log.error(f"Error creating tour package: {str(err)}")
            return Response({
                'status': 'error',
                'message': 'Unable to udpate tour package. Please try again.',
                'devMsg': str(err)
            }, status=status.HTTP_400_BAD_REQUEST)    
    
    @transaction.atomic
    def change_package_status(self, payload):
        try:
            package = TourPackage.objects.get(torp_id =payload.get('id'))
            package.torp_status=payload.get('status')
            package.save()
            return Response({
                'status': 'success',
                'message': 'Tour package status updated successfully.',
                'package_id': package.torp_id
            }, status=status.HTTP_201_CREATED)

        
        except Exception as err:
            transaction.set_rollback(True)
            self.log.error(f"Error creating tour package: {str(err)}")
            return Response({
                'status': 'error',
                'message': 'Unable to udpate tour package status. Please try again.',
                'devMsg': str(err)
            }, status=status.HTTP_400_BAD_REQUEST)    
         
    @transaction.atomic
    def packages_tabledata(self, request):
        try:
            draw = int(request.data.get('draw', 1))
            start = int(request.data.get('start', 0))
            length = int(request.data.get('length', 10))

            ordering_idx = int(request.data.get('order[0][column]', 0))
            ordering_col = request.data.get(f'columns[{ordering_idx}][data]', 'cusr_id')
            ordering_dir = request.data.get('order[0][dir]', 'desc')

            filter_torp_id = request.data.get('columns[0][search][value]')
            filter_torp_status = request.data.get('columns[1][search][value]')
            filter_torp_name = request.data.get('columns[2][search][value]')
            filter_state_date = request.data.get('columns[3][search][value]')
            filter_end_date = request.data.get('columns[4][search][value]')
            filter_from_price = request.data.get('columns[5][search][value]')
            filter_to_price = request.data.get('columns[6][search][value]')

            queryset = TourPackage.objects.exclude(torp_status='DL')

            # Apply filters
            if filter_torp_id:
                queryset = queryset.filter(cusr_id__icontains=filter_torp_id)
            if filter_torp_status:
                queryset = queryset.filter(cusr_is_verified=filter_torp_status)

            if filter_torp_name:
                queryset = queryset.filter(cusr_full_name__icontains=filter_torp_name)
            if filter_state_date:
                queryset = queryset.filter(cusr_mobile__icontains=filter_state_date)
            if filter_to_price:
                queryset = queryset.filter(cusr_email__icontains=filter_to_price)

            if filter_end_date:
                queryset = queryset.filter(cusr_created_at__gte=filter_end_date)
            if filter_from_price:
                queryset = queryset.filter(cusr_created_at__lte=filter_from_price)
                
            if filter_from_price:
                queryset = queryset.filter(cusr_created_at__lte=filter_from_price)    

            total_count = queryset.count()

            # Ordering
            if ordering_dir == 'asc':
                queryset = queryset.order_by(ordering_col)
            else:
                queryset = queryset.order_by('-' + ordering_col)

            queryset = queryset[start:start + length]

            serializer = TourPackageSerializer(queryset, many=True)

            return Response({
                'recordsFiltered': total_count,
                'recordsTotal': total_count,
                'draw': draw,
                'data': serializer.data,
                'status': 'success'
            })

        except Exception as e:
            return Response({
                'data': [],
                'status': 'error',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
     
     
    @transaction.atomic
    def get_all_tour_packages(self, torp_id , torp_name):
        try:
            queryset = TourPackage.objects.exclude(torp_status='DL')
            if torp_id:
                queryset = queryset.filter(torp_id=torp_id)
            if torp_name:
                queryset = queryset.filter(torp_name__icontains=torp_name)
            serializer = TourPackageSerializer(queryset, many=True)
            return Response({
                'message':"Get packages successfully.",
                'data': serializer.data,
                'status': 'success'
            })

        except Exception as e:
            return Response({
                'message':'enable to get packages',
                'data': [],
                'status': 'error',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
      
