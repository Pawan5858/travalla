import json
from django.contrib.auth import authenticate
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.response import Response
from apps.utils.enums import *
from apps.accounts.models import *
from rest_framework import status
from django.shortcuts import get_object_or_404
from apps.utils.utility import *
from rest_framework.exceptions import NotFound
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken


from rest_framework_simplejwt.exceptions import TokenError

class SessionHandler():
    
    def verifyMainUserSession(self, request, sessionFrom='headers'):
        # import pdb;pdb.set_trace();
        try:
            if sessionFrom == 'headers':
                token = request.headers.get('sessiontoken')
            elif sessionFrom == 'cookies':
                token = request.COOKIES.get('sessiontoken')

            if not token:
                return None

            try:
                # sessiontoken = Utility().decryptRSAString(token)
                jwttoken = AccessToken(token)
                # if not sessiontoken:
                #     return None
                if not jwttoken:
                    return None
                
                # userObj = json.loads(sessiontoken)
                user_id = jwttoken['user_id']

                user_obj = get_object_or_404(User, id=user_id)

                if user_obj.id == user_id:
                    return {
                        'user_id': user_obj.id,
                        'username': user_obj.username,
                        'email': user_obj.email,
                        'password': user_obj.password,
                        'user_type':user_obj.user_type
                    }
                else:
                    return None
            except TokenError as token_error:
                # Handle TokenError, e.g., token is invalid or expired
                return None

        except Exception as err:
            # Handle other exceptions if needed
            return None
    
  
    # def verifyMainUserSession(self, request, sessionFrom='headers'):
    #     # import pdb;pdb.set_trace();
    #     try:
    #         if sessionFrom == 'headers':
    #             token = request.headers.get('sessiontoken')
    #         elif sessionFrom == 'cookies':
    #             token = request.COOKIES.get('sessiontoken')

    #         if not token:
    #             return None

    #         try:
    #             # sessiontoken = Utility().decryptRSAString(token)
    #             if not sessiontoken:
    #                 return None
                
    #             userObj = json.loads(sessiontoken)
    #             sessiontoken = AccessToken(token)
    #             user_id = sessiontoken.payload['user_id']
                

    #             user_obj = get_object_or_404(User, id=userObj['id'])

    #             if user_obj.id == userObj['id']:
    #                 return {
    #                     'user_id': user_obj.id,
    #                     'username': user_obj.username,
    #                     'email': user_obj.email,
    #                     'password': user_obj.password,
    #                     'user_type':user_obj.user_type
    #                 }
    #             else:
    #                 return None
    #         except TokenError as token_error:
    #             # Handle TokenError, e.g., token is invalid or expired
    #             return None

    #     except Exception as err:
    #         # Handle other exceptions if needed
    #         return None


    def verifyCustomerSession(self, request, sessionFrom='headers'):
            try:
                if sessionFrom == 'headers':
                    token = request.headers.get('swcsessiontoken')
                elif sessionFrom == 'cookies':
                    token = request.COOKIES.get('swcsessiontoken')

                if not token:
                    return None

                # Decode the JWT token to extract the user ID
                decoded_token = AccessToken(token)
                user_id = decoded_token['customer_id']

                # Retrieve the customer object from the database
                customer_obj = Customers.objects.filter(cust_id=user_id).first()

                if not customer_obj:
                    return None
                
                # Serialize the customer object
                serializer = CustomersSerializer(customer_obj)
                serialized_data = serializer.data
                
                return serialized_data

            except TokenError as token_error:
                # Handle token error, e.g., token is invalid or expired
                if isinstance(token_error, InvalidToken) and token_error.args[0] == 'Token has expired':
                    return {'error': 'Token expired'}
                else:
                    raise token_error

            except Exception as err:
                # Handle other exceptions if needed
                raise NotFound("Failed to verify customer session.")

# ok
    # def verifyCustomerSession(self, request, sessionFrom='headers'):
    #     # import pdb;pdb.set_trace();
    #     try:
    #         if sessionFrom == 'headers':
    #             token = request.headers.get('swcsessiontoken')
    #         elif sessionFrom == 'cookies':
    #             token = request.COOKIES.get('swcsessiontoken')

    #         if not token:
    #             return None
    #         # Decode the JWT token to extract the user ID
    #         decoded_token = AccessToken(token)
    #         user_id = decoded_token['customer_id']

    #         # Retrieve the customer object from the database
    #         customer_obj = Customers.objects.filter(cust_id=user_id).first()

    #         if not customer_obj:
    #             return None
            
    #         # Serialize the customer object
    #         serializer = CustomersSerializer(customer_obj)
    #         serialized_data = serializer.data
            
    #         return serialized_data
    #     except Exception as err:
    #         # Handle exceptions if needed
    #         raise NotFound("Failed to verify customer session.")

    #     # def verifyCustomerSession(self, request, sessionFrom='headers'):
    #     #     # import pdb;pdb.set_trace();
    #     #     try:
    #     #         if sessionFrom == 'headers':
    #     #             token = request.headers.get('swcsessiontoken')
    #     #         elif sessionFrom == 'cookies':
    #     #             token = request.COOKIES.get('swcsessiontoken')

    #     #         if not token:
    #     #             return None

    #     #         try:
    #     #             sessiontoken = Utility().decryptRSAString(token)
    #     #             if not sessiontoken:
    #     #                 return None
                    
    #     #             userObj = json.loads(sessiontoken)
    #     #             # sessiontoken = AccessToken(token)
    #     #             # user_id = sessiontoken.payload['user_id']
                    

    #     #             user_obj = get_object_or_404(Customer, cust_id=userObj['id'])

    #     #             if user_obj.cust_id == userObj['id']:
    #     #                 return {
    #     #                     'cust_id': user_obj.cust_id,
    #     #                     'cust_firstname': user_obj.cust_firstname,
    #     #                     'cust_email': user_obj.cust_email  
    #     #                 }
    #     #             else:
    #     #                 return None
    #     #         except TokenError as token_error:
    #     #             # Handle TokenError, e.g., token is invalid or expired
    #     #             return None

    #     #     except Exception as err:
    #     #         # Handle other exceptions if needed
    #     #         return None


    def verifyTransportUserSession(self, request, sessionFrom='headers'):
        # import pdb;pdb.set_trace();
        try:
            if sessionFrom == 'headers':
                token = request.headers.get('swcsessiontoken')
            elif sessionFrom == 'cookies':
                token = request.COOKIES.get('sessiontoken')

            if not token:
                return None

            try:
                sessiontoken = Utility().decryptRSAString(token)
                if not sessiontoken:
                    return None
                
                userObj = json.loads(sessiontoken)
                # sessiontoken = AccessToken(token)
                # user_id = sessiontoken.payload['user_id']
                

                user_obj = get_object_or_404(TransportUsers, trnsu_id=userObj['id'])

                if user_obj.trnsu_id == userObj['id']:
                    return {
                        'trnsu_id': user_obj.trnsu_id,
                        'trnsu_firstname': user_obj.trnsu_firstname,
                        'trnsu_email': user_obj.trnsu_email  
                    }
                else:
                    return None
            except TokenError as token_error:
                # Handle TokenError, e.g., token is invalid or expired
                return None

        except Exception as err:
            # Handle other exceptions if needed
            return None

