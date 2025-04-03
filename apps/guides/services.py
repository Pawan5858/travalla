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

class guidesServices(object):
    def __init__(self):
        self.utility = Utility()
        self.log =logging.getLogger(__name__)
        
    @transaction.atomic
    def registerGuideUser(self, request):
        try:
            payload =request.data
            
            gude_image =request.FILES.get('image')
            
            if gude_image:
                if gude_image.name == '':
                    transaction.set_rollback(True)
                    return {'status': 'error', 'message': 'Please add a valid image file.'}
                image_filename = Utility().generateSecureFileNameAndSave('travellers_images' , gude_image)
            
            password_length = 4
            password = ''.join(random.choices(string.digits, k=password_length))
            hashed_password = make_password(password)
            
            # Check if user already exists
            if Guides.objects.filter(gude_email=payload['email']).exists():
                return Response({
                    'status': 'error',
                    'message': 'Email already registered'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            if Guides.objects.filter(gude_mobile=payload['mobile']).exists():
                return Response({
                    'status': 'error',
                    'message': 'Phone number already registered'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Prepare traveler data
            guide_data = {
            'gude_full_name': payload['name'],
            'gude_age': payload['age'],
            'gude_email': payload['email'],
            'gude_mobile': payload['mobile'],
            'gude_password_hash': hashed_password,
            'gude_profile_image': image_filename,
            'gude_type': payload['types'],
            'gude_has_car' : payload['car']
            }
            
            # Create new traveler guide
            guide_users = Guides.objects.create(**guide_data)
            
            # guide languages
            languages =json.loads(payload.get('languages', '[]')) 
            for lang in languages:
                lang = Languages.objects.get(lang_id=lang)
                GuideLanguages.objects.create(
                    gdln_gude =guide_users,
                    gdln_lang = lang
                )
                
            
            
            # guide skils
            skills =json.loads(payload.get('skills', '[]')) 
            for obj in skills:
                skill = Skills.objects.get(skil_id=obj)
                GuideSkills.objects.create(
                    gdsk_gude =guide_users,
                    gdsk_skill = skill
                )
            
            
            customer_details = {
                    'name': payload['name'],
                    'mobile': payload.get('mobile'),
                    'email': payload['email'],
                    'pwd': password
                }
            
            email_subject = 'Registration Confirmation'
            
            email_body = render_to_string("customer_registration_template.html", {
                'name': guide_users['gude_full_name'],
                'email': guide_users('gude_email'),
                'mobile': guide_users['gude_mobile'],
                'pwd': password
            })

            mail_send = send_mail(email_subject, '', settings.DEFAULT_FROM_EMAIL, [customer_details['email']], html_message=email_body)
            sms_send = Utility().send_textlocal_sms(customer_details)
        
            return Response({
                'status': 'success',
                'message': 'Guide registered successfully.'
            }, status=status.HTTP_201_CREATED)

        except Exception as err:
            transaction.set_rollback(True)
            self.log.error(f"Error creating contest: {str(err)}")
            return Response({
                'status': 'error',
                'message': 'Unable to registered . Please try again.',
                'devMsg': str(err)
            }, status=status.HTTP_400_BAD_REQUEST)
            
            
    @transaction.atomic
    def loginGuide(self, payload):
        try:
            user = Guides.objects.filter(gude_email=payload.get("username")).first()
            if not user:
                user = Guides.objects.filter(gude_mobile=payload.get("username")).first()

            if not user:
                return Response({'status': 'error', 'message': "Email/Mobile doesn't exist."}, status=status.HTTP_404_NOT_FOUND)
            
            
            # check the approved status

            
            decrypted_pwd = Utility().decryptRSAString(payload.get('password'))
            
            # Check password
            if not check_password(decrypted_pwd, user.gude_password_hash):
                return Response({'status': 'error', 'message': "Invalid Password."}, status=status.HTTP_401_UNAUTHORIZED)
            
            user.gude_fcm_token = payload.get("fcm_token")
            user.save()  # Save the user object to update the FCM token
            
            
            # Serialize user data
            serializer = GuidesSerializer(user)
           
            user_data = {
                'gude_id': user.gude_id,
                'gude_email': serializer.data['gude_email'],
                'gude_mobile': serializer.data['gude_mobile']
            }
            
            jwt_token = get_tokens_for_user(user_data)
            
            return Response({
                'status': 'success',
                'message': 'Logged in successfully.',
                'user': user_data,
                'token': jwt_token
            }, status=status.HTTP_200_OK)

        except Exception as err:
            transaction.set_rollback(True)
            self.log.error(f"Error creating contest: {str(err)}")
            return Response({
                'status': 'error',
                'message': 'Unable to login . Please try again.',
                'devMsg': str(err)
            }, status=status.HTTP_400_BAD_REQUEST)
    
    @transaction.atomic
    def approved_guides_table_data(self, request):
        try:
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

            queryset = Guides.objects.filter(gude_is_verified='APR').all()

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
    def un_approved_guides_table_data(self, request):
        try:
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

            queryset = Guides.objects.filter(gude_is_verified='NYA').all()

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
     