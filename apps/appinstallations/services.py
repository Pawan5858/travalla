# python builtins
import logging
import logging.config
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


def get_tokens_for_user(user):
    
    refresh = RefreshToken()
    refresh['id'] = user['trvl_id']
    refresh['mobile'] = user['trvl_mobile']  # Include any additional user information you need
    refresh['email'] = user['trvl_mobile']
    
    access_token = refresh.access_token
    refresh_token = str(refresh)

    return {
        'access': str(access_token),
        'refresh': refresh_token,
    }

class appInstallationsServices(object):
    def __init__(self):
        self.utility = Utility()
        self.log =logging.getLogger(__name__)
        
    @transaction.atomic
    def app_installation(self, payload):
        try:
            app_obj = AppInstallation.objects.filter(appi_uniqid =payload.get("uniqid")).first()
            if not app_obj:
                installation_data = {
                    'appi_catg': payload.get('appi_catg'),
                    'appi_uniqid': payload.get('appi_uniqid'),
                    'appi_device_act': payload.get('appi_device_act'),
                    'appi_appversion': payload.get('appi_appversion'),
                    'appi_devicetype': payload.get('appi_devicetype'),
                    'appi_devicemodel': payload.get('appi_devicemodel'),
                    'appi_devicemake': payload.get('appi_devicemake'),
                    'appi_deviceos': payload.get('appi_deviceos'),
                    'appi_deviceosversion': payload.get('appi_deviceosversion'),
                    'appi_pntoken': payload.get('appi_pntoken'),
                }
                
                installation = AppInstallation.objects.create(**installation_data)
            else:
                app_obj.appi_catg =payload.get('appi_catg')
                app_obj.appi_device_act = payload.get('appi_device_act')
                app_obj.appi_appversion = payload.get('appi_appversion')
                app_obj.appi_devicetype = payload.get('appi_devicetype')
                app_obj.appi_devicemodel = payload.get('appi_devicemodel')
                app_obj.appi_devicemake = payload.get('appi_devicemake')
                app_obj.appi_deviceos = payload.get('appi_deviceos')
                app_obj.appi_deviceosversion = payload.get('appi_deviceosversion')
                app_obj.appi_pntoken =payload.get('appi_pntoken')
                app_obj.save()

            return Response({
                'status': 'success',
                'message': 'App installation recorded successfully.',
                # 'data': {
                #     'appi_uniqid': installation.appi_uniqid,
                #     'appi_idate': installation.appi_idate
                # }
            }, status=status.HTTP_201_CREATED)

        except Exception as err:
            transaction.set_rollback(True)
            self.log.error(f"Error creating app installation: {str(err)}")
            return Response({
                'status': 'error',
                'message': 'Unable to record app installation. Please try again.',
                'devMsg': str(err)
            }, status=status.HTTP_400_BAD_REQUEST)
    
    @transaction.atomic
    def app_installation_table_data(self, request):
        try:
            draw = int(request.data.get('draw', 1))
            start = int(request.data.get('start', 0))
            length = int(request.data.get('length', 10))

            ordering_idx = int(request.data.get('order[0][column]', 0))
            ordering_col = request.data.get(f'columns[{ordering_idx}][data]', 'appi_id')
            ordering_dir = request.data.get('order[0][dir]', 'desc')

            filter_instl_id = request.data.get('columns[0][search][value]')
            filter_instl_status = request.data.get('columns[1][search][value]')
            filter_instl_name = request.data.get('columns[2][search][value]')
            filter_instl_mobile = request.data.get('columns[3][search][value]')
            filter_instl_lo_date_from = request.data.get('columns[4][search][value]')
            filter_instl_lo_date_to = request.data.get('columns[5][search][value]')
            filter_instl_email = request.data.get('columns[6][search][value]')

            queryset = AppInstallation.objects.all()

            # Apply filters
            if filter_instl_id:
                queryset = queryset.filter(cusr_id__icontains=filter_instl_id)
            if filter_instl_status:
                queryset = queryset.filter(cusr_is_verified=filter_instl_status)

            if filter_instl_name:
                queryset = queryset.filter(cusr_full_name__icontains=filter_instl_name)
            if filter_instl_mobile:
                queryset = queryset.filter(cusr_mobile__icontains=filter_instl_mobile)
            if filter_instl_lo_date_from:
                queryset = queryset.filter(cusr_email__icontains=filter_instl_lo_date_from)

            if filter_instl_lo_date_to:
                queryset = queryset.filter(cusr_created_at__gte=filter_instl_lo_date_to)
            if filter_instl_email:
                queryset = queryset.filter(cusr_created_at__lte=filter_instl_email)

            total_count = queryset.count()

            # Ordering
            if ordering_dir == 'asc':
                queryset = queryset.order_by(ordering_col)
            else:
                queryset = queryset.order_by('-' + ordering_col)

            queryset = queryset[start:start + length]

            serializer = AppInstallationSerializer(queryset, many=True)

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
    def un_approved_guides_table_data(self, request):
        try:
            # import pdb;
            # pdb.set_trace()
            draw = int(request.data.get('draw', 1))
            start = int(request.data.get('start', 0))
            length = int(request.data.get('length', 10))

            ordering_idx = int(request.data.get('order[0][column]', 0))
            ordering_col = request.data.get(f'columns[{ordering_idx}][data]', 'cusr_id')
            ordering_dir = request.data.get('order[0][dir]', 'desc')

            filter_gude_id = request.data.get('columns[0][search][value]')
            filter_gude_status = request.data.get('columns[1][search][value]')
            filter_gude_name = request.data.get('columns[2][search][value]')
            filter_gude_mobile = request.data.get('columns[3][search][value]')
            filter_gude_lo_date_from = request.data.get('columns[4][search][value]')
            filter_gude_lo_date_to = request.data.get('columns[5][search][value]')
            filter_gude_email = request.data.get('columns[6][search][value]')

            queryset = Guides.objects.filter(gude_is_verified='YTA').all()

            # Apply filters
            if filter_gude_id:
                queryset = queryset.filter(cusr_id__icontains=filter_gude_id)
            if filter_gude_status:
                queryset = queryset.filter(cusr_is_verified=filter_gude_status)

            if filter_gude_name:
                queryset = queryset.filter(cusr_full_name__icontains=filter_gude_name)
            if filter_gude_mobile:
                queryset = queryset.filter(cusr_mobile__icontains=filter_gude_mobile)
            if filter_gude_email:
                queryset = queryset.filter(cusr_email__icontains=filter_gude_email)

            if filter_gude_lo_date_from:
                queryset = queryset.filter(cusr_created_at__gte=filter_gude_lo_date_from)
            if filter_gude_lo_date_to:
                queryset = queryset.filter(cusr_created_at__lte=filter_gude_lo_date_to)

            total_count = queryset.count()

            # Ordering
            if ordering_dir == 'asc':
                queryset = queryset.order_by(ordering_col)
            else:
                queryset = queryset.order_by('-' + ordering_col)

            queryset = queryset[start:start + length]

            serializer = GuidesSerializer(queryset, many=True)

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
    def change_apr_status(self, payload):
        try:
            import pdb;
            pdb.set_trace()
            # Get customer
            guide_obj = Guides.objects.get(gude_id=payload['id'])  # Assuming 'gude_id' is correct in your model

            guide_obj.gude_is_verified = 'APR'  # Fixed assignment spacing
            guide_obj.save()

            return Response({
                'status': 'success',
                'message': 'Status Update successfully.'
            }, status=status.HTTP_200_OK)

        except Exception as err:
            transaction.set_rollback(True)
            logger.error(f"Error in resending OTP: {str(err)}")
            return Response({
                'status': 'error',
                'message': 'Unable to Update status. Please try again.',
                'devMsg': str(err)
            }, status=status.HTTP_400_BAD_REQUEST)