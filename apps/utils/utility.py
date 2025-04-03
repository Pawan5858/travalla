import os
from logging import getLogger
import hashlib
from Crypto.PublicKey import RSA # type: ignore
from Crypto.Cipher import PKCS1_v1_5 # type: ignore
import base64
import requests
import urllib.request
import urllib.parse
import hashlib
import binascii
import os  
import json
# fire base modules
import firebase_admin # type: ignore
from firebase_admin import credentials # type: ignore
from firebase_admin import messaging # type: ignore
from rest_framework.response import Response
from rest_framework import status
from apps.security.models import *
from apps.utils.enums import *
from django.conf import settings
from Travella.config import *
import logging
import logging.config
from django.conf import settings
logger = logging.getLogger(__name__)


class Utility():

    #=======================================================================================================
    #    Get Payment Gateway Config details
    #=======================================================================================================

    def getPaymentGatewayConfig(self, bank_acc_id):
        bank_account = BankAccount.objects .filter(baac_id=bank_acc_id).values(
                id=models.F('baac_id'),
                gateway=models.F('baac_gateway'),
                mode=models.F('baac_mode'),
                api_key=models.F('baac_api_key'),
                api_secret=models.F('baac_api_secret'),
                type=models.F('baac_type'),
                salt_key=models.F('baac_salt_key')).first()

        return bank_account


    def composePushNotificationText(self,msgType):
        # import pdb;pdb.set_trace();
        if msgType == "DRVR_ORDR":
            title = "SWC Order Received"
            msg = "Hi Driver, you have received an order!"
            message = {
                        "title": title,
                        "msg": msg
                    }
        
        elif msgType == "CUST_ORDR":
            title = "Thank you for your order"
            msg = "Dear Customer, We've received your order #180, it is now being processed. And your payment of Rs. 1800 was successful. Thank you for SWC"
            message = {
                        "title": title,
                        "msg": msg
                    }
       
        elif msgType == "OPTR_ORDR":
            title = "You have received an order"
            msg = "Hi Associate, you have received an order!"
            message = {
                        "title": title,
                        "msg": msg
                    }
        
        else:
            message = "Dear Customer, We've received your order #180, it is now being processed. And your payment of Rs. 1800 was successful. Thank you for shopping at Chikitsayam"
        return message

    def sendPushNotification(self, title, msg, registration_token, dataObject):
        # import pdb;pdb.set_trace();
        # Check if the default Firebase app is already initialized
        if not firebase_admin._apps:
            
            # cred = credentials.Certificate("E:/.nagaraju/Python/django_projects_backend/trip/serviceAccountKey.json")
            # cred = credentials.Certificate("/mnt/project/swc_te/serviceAccountKey.json")  
            # cred = credentials.Certificate("//192.168.108.10/swc_te/serviceAccountKey.json")
            # cred = credentials.Certificate("E:/.nagaraju/Python/django_projects_backend/_swc_date_wise/swc_29_7/serviceAccountKey.json")
            # cred = credentials.Certificate("E:\.pawan\swc\serviceAccountKey.json") 
            cred = credentials.Certificate("/var/www/html/swc/serviceAccountKey.json")
            firebase_admin.initialize_app(cred)

        # Ensure dataObject contains only string values
        dataObject = {k: str(v) for k, v in dataObject.items()}

        message = messaging.MulticastMessage(
            notification=messaging.Notification(
                title=title,
                body=msg
            ),
            data=dataObject,
            tokens=registration_token,
        )

        # Send a message to the device corresponding to the provided registration token.
        response = messaging.send_multicast(message)
        print('Successfully sent message:', response)


    def sendWebPushNotification(self, user_fcm_token):
        registration_ids = [user_fcm_token]

        message_title = "Order Recevied"
        message_desc = "Oreder Recevied To alert the vehicle"
        click_action_url = baseURL + "orders/"

        fcm_api = "AAAAFHtUKFU:APA91bEbRw-AlRniyevPGw0equXusE1KjbErmzHO6t1EfHze1xl8TEIHeijJdl5RGKEkQMb_AYOWe-FplWrDnCJT7HssUL7pJI0qA8r6AEQc6QLDoKpATsfTO363BnjJmarqsmBugW_e"
        url = "https://fcm.googleapis.com/fcm/send"

        headers = {
            "Content-Type": "application/json",
            "Authorization": 'key=' + fcm_api
        }

        payload = {
            "registration_ids": registration_ids,
            "priority": "high",
            "notification": {
                "body": message_desc,
                "title": message_title,
                "image": "http://192.168.108.10:8001/static/images/logos/swc_logo.png",
                "icon": "http://192.168.108.10:8001/static/images/logos/swc_logo.png",
                "click_action": click_action_url
            }
        }

        response = requests.post(url, data=json.dumps(payload), headers=headers)

        print("*******************")
        print(response)
        print("*******************")

        try:
            response.raise_for_status()  # Check if the request was successful
            print(response.json())       # Attempt to parse the response as JSON
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            print(f"Response content: {response.text}")
        except json.JSONDecodeError as json_err:
            print(f"JSON decode error: {json_err}")
            print(f"Response content: {response.text}")
        except Exception as err:
            print(f"An error occurred: {err}")
            print(f"Response content: {response.text}")



    def generateRSAKeys(self):
        key = RSA.generate(1024)
        publickey = key.publickey().exportKey('PEM')
        privatekey = key.exportKey('PEM')
        # print(publickey)
        # print(privatekey)
        return {}
    
    def generateRSAShow(self):
        key = b'-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC9ITaISnuVTdhWW0008bVKqwMF\nEkxBB4dA0svzCuQMmRXCZ9EFP8PL4VVqsju3lNdcpgRa8MzwCPRJ932+M7d6WNPz\nfHoF/nK85//sVQdHCj0rF5PDfvTGOnDeYvN/cdI/cnqQCsSb5ThqO/lr5w+hPuPq\nri1okYc3yE2cWaYHSQIDAQAB\n-----END PUBLIC KEY-----'
        key2 = b'-----BEGIN RSA PRIVATE KEY-----\nMIICXQIBAAKBgQC9ITaISnuVTdhWW0008bVKqwMFEkxBB4dA0svzCuQMmRXCZ9EF\nP8PL4VVqsju3lNdcpgRa8MzwCPRJ932+M7d6WNPzfHoF/nK85//sVQdHCj0rF5PD\nfvTGOnDeYvN/cdI/cnqQCsSb5ThqO/lr5w+hPuPqri1okYc3yE2cWaYHSQIDAQAB\nAoGAFp4ptNvfcqgIFq+9iHbdfOv9pPYeu2ookSaEcHDde+o00XZz50JMao3slqFx\nBc/df311KOECSTRw7oWT+pKZvunAN95ncJpgKdrcprSGM9dMv/Ak9Hsn2Anu6lJ4\nQHTCEIsfWPmS6R/Mk8+lJCrjxWgvVBDevMBz78YK8+DzWo8CQQDSJWijKKsyd3nU\nX1/dZWLBQqMpqMnyzS8rZ/2rmm5j1veDRRucBZmeDiGepUZVtQXrqIxTMLolSxKD\nNIsVAXtXAkEA5mXYjSLwjG0N1ZlYHk0A9qno5PSKhU0Qp+KJ8w3pDtBVwuNV7W9m\nywE0qo8YF9TbP72Ol8e62FQc+Vw542mOXwJBAIdKLiNce1ryMCzZeg4+x2VEUWbw\nk5MNJeD8AgQIWClOq+qHA09fC5cF4f8QyEdFU5pz2GN2a2C3BCQUH7ZWTeECQQCZ\nJbvDXSU+gsL+Z7beNVtdmuWXQ0HMh8R5hCkkaeuwECXhrNGSSUmvyTZj5UgjlzbB\n8NOW6om1gHvd+UL1elXLAkBGjYLMm1D8H3fHtFWcFQQMIMuO7YT+VheeWE7yIWxs\nPKOScBsWAyoQL90ypYlIMtkg29WQgI9HCsIEWciNinlh\n-----END RSA PRIVATE KEY-----'
        
        publickey = RSA.importKey(key)
        privatekey = RSA.importKey(key2)
        
        encryptor = PKCS1_v1_5.new(publickey)
        decryptor = PKCS1_v1_5.new(privatekey)
        
        ciphertext = encryptor.encrypt('encrypt this message'.encode('utf8'))
        encryptedStr = base64.b64encode(ciphertext).decode('ascii')
        # print(encryptedStr)
        
        ciphertext = base64.b64decode(encryptedStr.encode('ascii'))
        plaintext = decryptor.decrypt(ciphertext, b'DECRYPTION FAILED')
        decryptedStr = plaintext.decode('utf8')
        # print(decryptedStr)
    
    def encryptToRSAString(self, reqStr):
        public_key = b'-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC9ITaISnuVTdhWW0008bVKqwMF\nEkxBB4dA0svzCuQMmRXCZ9EFP8PL4VVqsju3lNdcpgRa8MzwCPRJ932+M7d6WNPz\nfHoF/nK85//sVQdHCj0rF5PDfvTGOnDeYvN/cdI/cnqQCsSb5ThqO/lr5w+hPuPq\nri1okYc3yE2cWaYHSQIDAQAB\n-----END PUBLIC KEY-----'
        
        publickey = RSA.importKey(public_key)
        
        encryptor = PKCS1_v1_5.new(publickey)
        ciphertext = encryptor.encrypt(reqStr.encode("utf-8"))
        
        return base64.b64encode(ciphertext).decode('ascii')
    
    def decryptRSAString(self, reqStr):
        private_key = b'-----BEGIN RSA PRIVATE KEY-----\nMIICXQIBAAKBgQC9ITaISnuVTdhWW0008bVKqwMFEkxBB4dA0svzCuQMmRXCZ9EF\nP8PL4VVqsju3lNdcpgRa8MzwCPRJ932+M7d6WNPzfHoF/nK85//sVQdHCj0rF5PD\nfvTGOnDeYvN/cdI/cnqQCsSb5ThqO/lr5w+hPuPqri1okYc3yE2cWaYHSQIDAQAB\nAoGAFp4ptNvfcqgIFq+9iHbdfOv9pPYeu2ookSaEcHDde+o00XZz50JMao3slqFx\nBc/df311KOECSTRw7oWT+pKZvunAN95ncJpgKdrcprSGM9dMv/Ak9Hsn2Anu6lJ4\nQHTCEIsfWPmS6R/Mk8+lJCrjxWgvVBDevMBz78YK8+DzWo8CQQDSJWijKKsyd3nU\nX1/dZWLBQqMpqMnyzS8rZ/2rmm5j1veDRRucBZmeDiGepUZVtQXrqIxTMLolSxKD\nNIsVAXtXAkEA5mXYjSLwjG0N1ZlYHk0A9qno5PSKhU0Qp+KJ8w3pDtBVwuNV7W9m\nywE0qo8YF9TbP72Ol8e62FQc+Vw542mOXwJBAIdKLiNce1ryMCzZeg4+x2VEUWbw\nk5MNJeD8AgQIWClOq+qHA09fC5cF4f8QyEdFU5pz2GN2a2C3BCQUH7ZWTeECQQCZ\nJbvDXSU+gsL+Z7beNVtdmuWXQ0HMh8R5hCkkaeuwECXhrNGSSUmvyTZj5UgjlzbB\n8NOW6om1gHvd+UL1elXLAkBGjYLMm1D8H3fHtFWcFQQMIMuO7YT+VheeWE7yIWxs\nPKOScBsWAyoQL90ypYlIMtkg29WQgI9HCsIEWciNinlh\n-----END RSA PRIVATE KEY-----'
        
        privatekey = RSA.importKey(private_key)
        
        decryptor = PKCS1_v1_5.new(privatekey)

        ciphertext = base64.b64decode(reqStr.encode('ascii'))
        plaintext = decryptor.decrypt(ciphertext, b'DECRYPTION FAILED')
        
        return plaintext.decode('utf8')


    #===========================================================================
    # This will Return the md5 hash of the password+salt 
    #===========================================================================
    # def hash_pass(self, password):
    #     """
    #     Return the md5 hash of the password+salt
    #     """
    #     salted_password = password + current_app.secret_key
    #     h = hashlib.md5(salted_password.encode())
    #     return h.hexdigest()

    # def hash_pass(self, password):
    #     """
    #     Return the sha256 hash of the password+salt
    #     """
    #     # Generate a random salt
    #     salt = binascii.hexlify(os.urandom(16)).decode()
        
    #     # Combine password and salt
    #     salted_password = password + salt

    #     # Hash the salted password using SHA-256
    #     h = hashlib.sha256(salted_password.encode()).hexdigest()

    #     # Store the salt and hashed password in the model
    #     self.salt = salt
    #     self.hashed_password = h
    
    def hash_pass(self, password):
        """
        Return the sha256 hash of the password+salt
        """
        # Generate a random salt
        salt = binascii.hexlify(os.urandom(16)).decode()
        
        # Combine password and salt
        salted_password = password + salt

        # Hash the salted password using SHA-256
        hashed_password = hashlib.sha256(salted_password.encode()).hexdigest()

        # Store the salt and hashed password in the model or return it
        # Depending on your use case, you might want to store it in your model
        # or return it to the calling code
        return hashed_password

    def check_password(self, password):
        """
        Check if the provided password matches the stored hashed password
        """
        # Combine provided password with stored salt
        salted_password = password + self.salt

        # Hash the salted password using SHA-256
        hashed_password = hashlib.sha256(salted_password.encode()).hexdigest()

        # Compare with the stored hashed password
        return hashed_password == self.hashed_password

    #===========================================================================
    # This will Return the SHA1 hash of the Given String
    #===========================================================================
    def hash_SHA1(self, word):
        """
        Return the SHA1 hash of the Given String
        """
        h = hashlib.sha1(word.encode())
        return h.hexdigest()
    
    #===========================================================================
    # This will Return the SHA512 hash of the Given String
    #===========================================================================
    def hash_SHA512(self,word):
        print("hashhhhh")
        print(word)
        """
        Return the SHA512 hash of the Given String
        """
        h = hashlib.sha512(word.encode())
        return h.hexdigest()
        

    #===========================================================================
    # This will Return Base64 String of image from given URL
    #===========================================================================
    def get_base64_from(self, url):
        return base64.b64encode(requests.get(url).content)
    
    #===========================================================================
    # This will Return get logistic types
    #===========================================================================
    def get_logistic_types(self):
        try:
            # Query all logistic types
            logistic_types = LogisticOperatorTypes.objects.all()

            # Serialize the queryset
            serializer = LogisticOperatorTypesSerializer(logistic_types, many=True)

            # Convert the serialized data to a list of dictionaries using a loop
            result_list = []
            for item in serializer.data:
                result_list.append(dict(item))

            # Return the list of dictionaries
            return result_list

        except Exception as e:
            # Handle exceptions appropriately
            return {'error': str(e)}

        
    def get_locations_cities(self):
        try:
            # Query all logistic types
            locations = Locations.objects.all()

            # Serialize the queryset
            serializer = LocationsSerializer(locations, many=True)

            # Convert the serialized data to a list of dictionaries using a loop
            result_list = []
            for item in serializer.data:
                result_list.append(dict(item))

            # Return the list of dictionaries
            return result_list

        except Exception as e:
            # Handle exceptions appropriately
            return {'error': str(e)}

    def get_cities(self):
        try:
            # Query all State 
            cities = Cities.objects.all()

            # Serialize the queryset
            serializer = CitiesSerializer(cities, many=True)

            # Convert the serialized data to a list of dictionaries using a loop
            result_list = []
            for item in serializer.data:
                result_list.append(dict(item))

            # Return the list of dictionaries
            return result_list

        except Exception as e:
            # Handle exceptions appropriately
            return {'error': str(e)}
        

    def get_operating_cities(self):
        try:
            # Query SWCOperatingCities to get city IDs
            operating_city_ids = SWCOperatingCities.objects.values_list('city_id', flat=True).distinct()

            # Query Cities to get city details for the retrieved IDs
            cities = Cities.objects.filter(city_id__in=operating_city_ids)

            # Serialize the queryset
            serializer = CitiesSerializer(cities, many=True)

            # Convert the serialized data to a list of dictionaries
            result_list = []
            for item in serializer.data:
                result_list.append(dict(item))

            # Return the list of dictionaries
            return result_list

        except Exception as e:
            # Handle exceptions appropriately
            return {'error': str(e)}

    def get_swcoperatingcity_swcserviceablelocations(self):
        try:
            # Query all city IDs from SWCOperatingCities
            operating_city_ids = SWCOperatingCities.objects.values_list('city_id', flat=True).distinct()

            # Query CityLocations to get all location IDs for operating city IDs
            all_city_location_ids = CityLocations.objects.filter(city_id__in=operating_city_ids).values_list('locn_id', flat=True)

            # Query SWCServiceableLocations to get location IDs that are serviceable
            all_serviceable_location_ids = SWCServiceableLocations.objects.filter(locn_id__in=all_city_location_ids).values_list('locn_id', flat=True)

            # Query Locations to get location details for the filtered IDs
            all_locations = Locations.objects.filter(pk__in=all_serviceable_location_ids)

            # Serialize the queryset
            serializer = LocationsSerializer(all_locations, many=True)

            # Convert the serialized data to a list of dictionaries
            result_list = []
            for item in serializer.data:
                result_list.append(dict(item))

            # Return the list of dictionaries
            return result_list

        except Exception as e:
            # Handle exceptions appropriately
            return {'error': str(e)}



    def get_locations(self):
        try:
            # Query all State 
            locations = State.objects.all()

            # Serialize the queryset
            serializer = StateSerializer(locations, many=True)

            # Convert the serialized data to a list of dictionaries using a loop
            result_list = []
            for item in serializer.data:
                result_list.append(dict(item))

            # Return the list of dictionaries
            return result_list

        except Exception as e:
            # Handle exceptions appropriately
            return {'error': str(e)}
        
    def get_swcservice(self):
        try:
            # Query all State 
            swcservices = SWCService.objects.all()

            # Serialize the queryset
            serializer = SWCServiceSerializer(swcservices, many=True)

            # Convert the serialized data to a list of dictionaries using a loop
            result_list = []
            for item in serializer.data:
                result_list.append(dict(item))

            # Return the list of dictionaries
            return result_list

        except Exception as e:
            # Handle exceptions appropriately
            return {'error': str(e)}


    #===========================================================================
    # This will Return get Document types
    #===========================================================================
    def get_document_types(self):
        try:
            # Query all logistic types
            document_types = DocumentTypes.objects.all()

            # Serialize the queryset
            serializer = DocumentTypesSerializer(document_types, many=True)

            # Convert the serialized data to a list of dictionaries using a loop
            result_list = []
            for item in serializer.data:
                result_list.append(dict(item))

            # Return the list of dictionaries
            return result_list

        except Exception as e:
            # Handle exceptions appropriately
            return {'error': str(e)}
    

    def get_sms_sender_details(self,sms_type = smsTypeEnum['transnational']):
        try:
     
            apikeys_record = SmsServiceProvider.objects.filter(sms_sptype=sms_type).first()

            if apikeys_record:
                return {
                    'sender_id': apikeys_record.sms_spsender,
                    'api_key': apikeys_record.sms_spapikey
                }
            else:
                return None

        except Exception as err:
            return None
        
    # =======================================================================================================
    #    Send TextLocal SMS with provided info
    # =======================================================================================================
    def send_textlocal_sms(self):
        try:
            sms_sender_id = 'NIMFRZ'
            sms_api_key = 'NGE3MjU0NDY3OTU1NmE0YTZkNzgzNzQ3NTI1Mjc0MzQ='
            api_key = sms_api_key
            sender_id = sms_sender_id
            base_url = settings.TXTLCL_BASE_URL  # Use the base URL from settings
            message = self.composeSMSText()

            data = urllib.parse.urlencode({
                'apikey': api_key,
                'numbers': '9573487851',  # Update with actual numbers
                'message': message,
                'sender': sender_id,
                'test': False
            }).encode('utf-8')

            txtlcl_request = urllib.request.Request(base_url)
            f = urllib.request.urlopen(txtlcl_request, data)
            fr = f.read()
            fr = json.loads(fr.decode('utf-8'))

            return Response(fr)

        except Exception as e:
            logger.error('An error occurred in send_textlocal_sms: %s', str(e), exc_info=True)
            return Response({'error': str(e)}, status=500)

    def composeSMSText(self):
        message = "Dear Customer, We've received your order #180, it is now being processed. And your payment of Rs. 1800 was successful. Thank you for shopping at Chikitsayam"
        return message


    def send_textlocal_sms(self,transport_user_details):
        try:
            # import pdb;pdb.set_trace();
            
            # textlocal_username=sreedhar@preciouscareers.com
            # TEXTLOCAL_APIKEY=Y4bbuDG2L7A-zrXzT6GjCV9IYFEeX1CZi3ZCJPsKzy
            # TEXTLOCAL_HASH=85059c0baf836ec1c4ad16751fdd45d79ea2ceab4968adfaadd29c52b7acd2e2
            # TEXTLOCAL_SENDER=NIDEMO
            # TEXTLOCAL_COUNTRY=IN
                        
            sms_sender_id = 'NIMFRZ'
            # sms_sender_id = 'NIDEMO'
            sms_api_key = 'NGE3MjU0NDY3OTU1NmE0YTZkNzgzNzQ3NTI1Mjc0MzQ='
            # sms_api_key = 'Y4bbuDG2L7A-zrXzT6GjCV9IYFEeX1CZi3ZCJPsKzy'
            api_key = sms_api_key
            sender_id = sms_sender_id
            base_url = settings.TXTLCL_BASE_URL  # Use the base URL from settings
            message = self.composeSMSText(transport_user_details)
            # message = self.composeSMSTextRegister()

            data = urllib.parse.urlencode({
                'apikey': api_key,
                'numbers': transport_user_details['mobile'],  # Update with actual numbers
                'message': message,
                'sender': sender_id,
                'test': False
            }).encode('utf-8')

            txtlcl_request = urllib.request.Request(base_url)
            f = urllib.request.urlopen(txtlcl_request, data)
            fr = f.read()
            fr = json.loads(fr.decode('utf-8'))

            return Response(fr)

        except Exception as e:
            logger.error('An error occurred in send_textlocal_sms: %s', str(e), exc_info=True)
            return Response({'error': str(e)}, status=500)

    def composeSMSText(self,transport_user_details):
        
        message = "Dear Customer, We've received your order #"+ str(transport_user_details['pwd']) +", it is now being processed. And your payment of Rs. 1800 was successful. Thank you for shopping at Chikitsayam"
        # message = "Your unique login verification code for Precious Career is " + str(transport_user_details['pwd'])
        return message

       
        # message = "Dear Customer, We've received your order #121, it is now being processed. And your payment of Rs. 1800 was successful. Thank you for shopping at Chikitsayam"
        # return message

    # working object
    def get_preferences_list(self, category):
        try:
            preferences = ConsoleOption.objects.filter(
                copt_category=category,
                copt_status='AC'
            ).values(
                'copt_id', 'copt_name',
                'copt_copc_id__copc_id', 'copt_copc_id__copc_name',
                'copt_copc_id__copc_parent_id__copc_id', 'copt_copc_id__copc_parent_id__copc_name'
            )

            result_array = []
            parent_categories_dict = {}

            for preference in preferences:
                parent_category_id = preference['copt_copc_id__copc_parent_id__copc_id'] or 0
                parent_category_name = preference['copt_copc_id__copc_parent_id__copc_name'] or None

                if parent_category_id not in parent_categories_dict:
                    parent_categories_dict[parent_category_id] = {
                        'id': parent_category_id,
                        'title': parent_category_name,
                        'categories': {}
                    }

                category_id = preference['copt_copc_id__copc_id'] or 0
                category_name = preference['copt_copc_id__copc_name'] or None

                if category_id not in parent_categories_dict[parent_category_id]['categories']:
                    parent_categories_dict[parent_category_id]['categories'][category_id] = {
                        'id': category_id,
                        'title': category_name,
                        'preferences': []
                    }

                preference_obj = {
                    'id': preference['copt_id'],
                    'title': preference['copt_name']
                }
                parent_categories_dict[parent_category_id]['categories'][category_id]['preferences'].append(preference_obj)

            result_array = list(parent_categories_dict.values())
            return result_array

        except Exception as err:
            logger.error('An error occurred in get_preferences_list: %s', str(err), exc_info=True)
            # Handle exceptions appropriately
            print(f"Error in get_preferences_list: {err}")
            return []


    def get_vehicle_types(self):
        try:
            # Query all vehicle types
            vehicle_types = VehicleType.objects.all()

            # Serialize the queryset
            serializer = VehicleTypeSerializer(vehicle_types, many=True)

            # Convert the serialized data to a list of dictionaries using a loop
            result_list = []
            for item in serializer.data:
                result_list.append(dict(item))

            # Return the list of dictionaries
            return result_list

        except Exception as e:
            logger.error('An error occurred in get_vehicle_types: %s', str(e), exc_info=True)
            # Handle exceptions appropriately
            return {'error': str(e)}


    def generateSecureFileNameAndSave(self, path, file):
        """ Generate a unique file name and save the file """
        
        # Combine the MEDIA_ROOT with the provided path
        full_path = os.path.join(settings.MEDIA_ROOT, path)
        
        # Ensure the directory exists
        os.makedirs(full_path, exist_ok=True)
        
        # Generate a unique filename
        filename = self.generateUniqueFilename(full_path, file.name)
        
        # Save the file
        file_path = os.path.join(full_path, filename)
        
        with open(file_path, "wb+") as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        return filename

    def generateUniqueFilename(self, base_path, filename, index=0):
        """ Generate a unique filename by appending a number if the file exists """
        name, ext = os.path.splitext(filename)
        new_filename = f"{name}_{index}{ext}" if index else filename

        if os.path.exists(os.path.join(base_path, new_filename)):
            return self.generateUniqueFilename(base_path, filename, index + 1)
        return new_filename