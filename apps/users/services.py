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
from .models import *
import random
import string
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import datetime, timedelta
from django.utils import timezone  # Add this import
logger = logging.getLogger(__name__)


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

class userServices(object):
    def __init__(self):
        self.utility = Utility()
        self.log =logging.getLogger(__name__)
        
    # @transaction.atomic
    # def registerCustomerUser(self, payload):
    #     try:
    #         otp_length = 4
    #         # Check if user already exists
    #         if Customerusers.objects.filter(cusr_email=payload['email'], cusr_is_verified='Y').exists():
    #             return Response({
    #                 'status': 'error',
    #                 'message': 'Email already registered.'
    #             }, status=status.HTTP_400_BAD_REQUEST)
            
    #         customer = Customerusers.objects.get(cusr_email=payload.get('email'))
    #         if customer.cusr_is_verified == 'N':
    #             otp = ''.join(random.choices(string.digits, k=otp_length))
    #             expires_at = datetime.now() + timedelta(minutes=10)
    #             customer.cusr_password_hash = make_password(payload.get('password'))
    #             customer.cust_otp = otp  # Update latest OTP in main table
    #             customer.save()
                
    #             OTP.objects.create(
    #                 user=customer,
    #                 otp_code=otp,
    #                 expires_at=expires_at
    #             )
                
    #             email_subject = 'otp verification'
                
    #             email_body = render_to_string("customer_registration_template.html", {
    #             'massage': 'verification otp.'
    #             })
                
    #             mail_send = send_mail(email_subject, '', settings.DEFAULT_FROM_EMAIL, [payload.get('email')], html_message=email_body)
             
            
            
                
            
    #         # Prepare traveler data
    #         cusrusers_data = {
    #         'cusr_full_name': payload['name'],
    #         'cusr_email': payload['email'],
    #         'cusr_password_hash': payload['password'],
    #         'cust_otp' : otp
    #         }

    #         # Create new traveler
    #         customer_users = Customerusers.objects.create(**cusrusers_data)
            
    #        # Add OTP to history table
    #         OTP.objects.create(
    #             user=customer,
    #             otp_code=otp,
    #             expires_at=expires_at
    #         )
            
    #         email_subject = 'otp verification'
    #         email_body = render_to_string("customer_registration_template.html", {
    #             'massage': 'verification otp.'
    #         })
            
            

    #         mail_send = send_mail(email_subject, '', settings.DEFAULT_FROM_EMAIL, [payload.get('email')], html_message=email_body)
    #         # sms_send = Utility().send_textlocal_sms(customer_details)
        
    #         return Response({
    #             'status': 'success',
    #             'message': 'User registered successfully.'
    #         }, status=status.HTTP_201_CREATED)

    #     except Exception as err:
    #         transaction.set_rollback(True)
    #         self.log.error(f"Error creating contest: {str(err)}")
    #         return Response({
    #             'status': 'error',
    #             'message': 'Unable to registered . Please try again.',
    #             'devMsg': str(err)
    #         }, status=status.HTTP_400_BAD_REQUEST)
    
   

    @transaction.atomic
    def registerCustomerUser(self, payload):
        try:
            otp_length = 4
            # Check if user already exists and is verified
            if Customerusers.objects.filter(cusr_email=payload['email'], cusr_is_verified='Y').exists():
                return Response({
                    'status': 'error',
                    'message': 'Email already registered.'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Generate OTP
            otp = ''.join(random.choices(string.digits, k=otp_length))
            expires_at = datetime.now() + timedelta(minutes=10)
            
            # Check for existing unverified user
            customer_exists = Customerusers.objects.filter(cusr_email=payload.get('email')).exists()
            
            if customer_exists:
                customer = Customerusers.objects.get(cusr_email=payload.get('email'))
                if customer.cusr_is_verified == 'N':
                    customer.cusr_password_hash = make_password(payload.get('password'))
                    customer.cust_otp = otp  # Update latest OTP in main table
                    customer.save()
                    
                    # Add OTP to history table
                    OTP.objects.create(
                        user=customer,
                        otp_code=otp,
                        expires_at=expires_at
                    )
                    
                    email_subject = 'otp verification'
                    
                    email_body = render_to_string("customer_registration_template.html", {
                        'massage': 'verification otp.',
                        'otp': otp,
                        'email':payload['email']
                    })
                    
                    mail_send = send_mail(email_subject, '', settings.DEFAULT_FROM_EMAIL, [payload.get('email')], html_message=email_body)
                    
                    return Response({
                        'status': 'success',
                        'message': 'Password updated and OTP sent for verification.'
                    }, status=status.HTTP_200_OK)
            else:
                cusrusers_data = {
                    'cusr_email': payload['email'],
                    'cusr_password_hash': make_password(payload['password']),
                    'cust_otp': otp
                }

                # Create new traveler
                customer = Customerusers.objects.create(**cusrusers_data)
                
                # Add OTP to history table
                OTP.objects.create(
                    user=customer,
                    otp_code=otp,
                    expires_at=expires_at
                )
                
                email_subject = 'otp verification'
                email_body = render_to_string("customer_registration_template.html", {
                    'massage': 'verification otp.',
                    'otp': otp,
                    'email':payload['email']
                })
                
                mail_send = send_mail(email_subject, '', settings.DEFAULT_FROM_EMAIL, [payload.get('email')], html_message=email_body)
                    
            
                return Response({
                    'status': 'success',
                    'message': 'User registered successfully.'
                }, status=status.HTTP_201_CREATED)

        except Exception as err:
            transaction.set_rollback(True)
            self.log.error(f"Error creating contest: {str(err)}")
            return Response({
                'status': 'error',
                'message': 'Unable to register. Please try again.',
                'devMsg': str(err)
            }, status=status.HTTP_400_BAD_REQUEST)
    
    

    @transaction.atomic
    def verifyOtp(self, payload):
        try:
            # Get customer
            customer = Customerusers.objects.get(cusr_email=payload['email'])
            
            # Check if already verified
            if customer.cusr_is_verified == 'Y':
                return Response({
                    'status': 'error',
                    'message': 'Account is already verified.'
                }, status=status.HTTP_400_BAD_REQUEST)
           
            # Check if OTP matches the latest one in Customerusers
            if customer.cust_otp != str(payload['otp']):
                return Response({
                    'status': 'error',
                    'message': 'Invalid OTP.'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Get OTP record from history table (use cust_otp length of 4)
            otp_record = OTP.objects.filter(user=customer, otp_code=payload['otp']).first()
            
            if not otp_record:
                return Response({
                    'status': 'error',
                    'message': 'OTP record not found.'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            
                
            # Check expiration and usage (use timezone.now() instead of datetime.now())
            if otp_record.is_used or otp_record.expires_at < timezone.now():
                return Response({
                    'status': 'error',
                    'message': 'OTP has expired or already used.'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Verify the customer
            customer.cusr_is_verified = 'Y'
            customer.cust_otp = None  # Clear the OTP after verification
            otp_record.is_used = True
            customer.save()
            otp_record.save()
            
            # Send confirmation email
            email_subject = 'Account Verified'
            email_body = render_to_string("otp_verification_template.html", {
                'massage': 'Your account has been successfully verified.',
                'email':payload['email']
            })
            
            mail_send = send_mail(
                email_subject,
                '',
                settings.DEFAULT_FROM_EMAIL,
                [payload['email']],
                html_message=email_body,
                fail_silently=False
            )
            
            return Response({
                'status': 'success',
                'message': 'Account verified successfully.'
            }, status=status.HTTP_200_OK)

        except Customerusers.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'User not found.'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as err:
            transaction.set_rollback(True)
            logger.error(f"Error in OTP verification: {str(err)}")
            return Response({
                'status': 'error',
                'message': 'Unable to verify OTP. Please try again.',
                'devMsg': str(err)
            }, status=status.HTTP_400_BAD_REQUEST)      
    
    @transaction.atomic
    def resendOtp(self, payload):
        try:
           
            # Get customer
            customer = Customerusers.objects.get(cusr_email=payload['email'])
            
            # Check if already verified
            if customer.cusr_is_verified == 'Y':
                return Response({
                    'status': 'error',
                    'message': 'Account is already verified. No OTP needed.'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Generate new OTP
            otp_length = 4
            otp = ''.join(random.choices(string.digits, k=otp_length))
            expires_at = timezone.now() + timezone.timedelta(minutes=10)
            
            # Update latest OTP in Customerusers
            customer.cust_otp = otp
            customer.save()
            
            # Add new OTP to history table
            OTP.objects.create(
                user=customer,
                otp_code=otp,
                expires_at=expires_at
            )
            
            # Send OTP email
            email_subject = 'OTP Verification - Resend'
            email_body = render_to_string("customer_registration_template.html", {
                'email': payload['email'],
                'otp': otp
            })
            
            mail_send = send_mail(
                email_subject,
                '',
                settings.DEFAULT_FROM_EMAIL,
                [payload['email']],
                html_message=email_body,
                fail_silently=False
            )
            
            return Response({
                'status': 'success',
                'message': 'New OTP sent successfully.'
            }, status=status.HTTP_200_OK)

        except Customerusers.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'User not found. Please register first.'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as err:
            transaction.set_rollback(True)
            logger.error(f"Error in resending OTP: {str(err)}")
            return Response({
                'status': 'error',
                'message': 'Unable to resend OTP. Please try again.',
                'devMsg': str(err)
            }, status=status.HTTP_400_BAD_REQUEST)
    
    @transaction.atomic
    def loginUser(self, payload):
        try:
            user = Customerusers.objects.filter(cusr_email=payload.get("username")).first()
            if not user:
                user = Customerusers.objects.filter(cusr_mobile=payload.get("username")).first()

           
            if not user:
                return Response({'status': 'error', 'message': "Email/Mobile doesn't exist."}, status=status.HTTP_404_NOT_FOUND)

            
            decrypted_pwd = Utility().decryptRSAString(payload.get('password'))
            
            # Check password
            if not check_password(decrypted_pwd, user.trvl_password):
                return Response({'status': 'error', 'message': "Invalid Password."}, status=status.HTTP_401_UNAUTHORIZED)
            
            user.cusr_fcm_token = payload.get("fcm_token")
            user.save()  # Save the user object to update the FCM token
            
            
            # Serialize user data
            serializer = CustomerusersSerializer(user)
           
            user_data = {
                'cusr_id': user.cusr_id,
                'cusr_email': serializer.data['cusr_email'],
                'cusr_mobile': serializer.data['cusr_mobile']
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
    def register_customers_table_data(self, request):
        try:
            draw = int(request.data.get('draw', 1))
            start = int(request.data.get('start', 0))
            length = int(request.data.get('length', 10))
            ordering_idx = int(request.data.get('order[0][column]', 0))
            ordering_col = request.data.get(f'columns[{ordering_idx}][data]', 'cusr_id')
            ordering_dir = request.data.get('order[0][dir]', 'desc')

            filter_cust_id = request.data.get('columns[0][search][value]')
            filter_cust_status = request.data.get('columns[1][search][value]')
            filter_customer_name = request.data.get('columns[2][search][value]')
            filter_customer_mobile = request.data.get('columns[3][search][value]')
            filter_cust_lo_date_from = request.data.get('columns[4][search][value]')
            filter_cust_lo_date_to = request.data.get('columns[5][search][value]')
            filter_customer_email = request.data.get('columns[6][search][value]')

            queryset = Customerusers.objects.filter(cusr_is_verified='Y').exclude(cusr_status='DL')

            # Apply filters
            if filter_cust_id:
                queryset = queryset.filter(cusr_id__icontains=filter_cust_id)
            if filter_cust_status:
                queryset = queryset.filter(cusr_is_verified=filter_cust_status)

            if filter_customer_name:
                queryset = queryset.filter(cusr_full_name__icontains=filter_customer_name)
            if filter_customer_mobile:
                queryset = queryset.filter(cusr_mobile__icontains=filter_customer_mobile)
            if filter_customer_email:
                queryset = queryset.filter(cusr_email__icontains=filter_customer_email)

            if filter_cust_lo_date_from:
                queryset = queryset.filter(cusr_created_at__gte=filter_cust_lo_date_from)
            if filter_cust_lo_date_to:
                queryset = queryset.filter(cusr_created_at__lte=filter_cust_lo_date_to)

            total_count = queryset.count()

            # Ordering
            if ordering_dir == 'asc':
                queryset = queryset.order_by(ordering_col)
            else:
                queryset = queryset.order_by('-' + ordering_col)

            queryset = queryset[start:start + length]

            serializer = CustomerusersSerializer(queryset, many=True)

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
    
