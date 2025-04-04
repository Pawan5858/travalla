from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from apps.accounts.serializers import *
from apps.utils.enums import *
from apps.utils.utility import *
from apps.utils.session_handler import *
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken # type: ignore
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import redirect
from apps.dashboard.views import *
from apps.utils.utility import *
from django.http import HttpResponse
# # Create your views here.

# def login(request):
#     return render(request,'login.html')


logger = logging.getLogger(__name__)



def settings_function(request,subdomain=None):
    side_menu = SideMenu()
    menu_list = side_menu.currentMenu(request)

    pageData = {
        'page_link': 'settings',
        'currentMenu': menu_list,
        'admin_console': 'MAIN_ADMIN' ,
    }

    # return render(request, 'logistic_operators/logistic_operators.html', {'pageData': pageData})
    return sendResponseScreen(request, subdomain, 'commingSoon.html', pageData)


def MIS_reports(request,subdomain=None):
    side_menu = SideMenu()
    menu_list = side_menu.currentMenu(request)

    pageData = {
        'page_link': 'reports',
        'sub_link' : 'mis-reports',
        'currentMenu': menu_list,
        'admin_console': 'MAIN_ADMIN' ,
    }

    # return render(request, 'logistic_operators/logistic_operators.html', {'pageData': pageData})
    return sendResponseScreen(request, subdomain, 'commingSoon.html', pageData)

def daily_reports(request,subdomain=None):
    side_menu = SideMenu()
    menu_list = side_menu.currentMenu(request)

    pageData = {
        'page_link': 'reports',
        'sub_link' : 'daily-reports',
        'currentMenu': menu_list,
        'admin_console': 'MAIN_ADMIN' ,
    }

    # return render(request, 'logistic_operators/logistic_operators.html', {'pageData': pageData})
    return sendResponseScreen(request, subdomain, 'commingSoon.html', pageData)

def showFirebaseJS(request):
    # import pdb;pdb.set_trace();
    data='importScripts("https://www.gstatic.com/firebasejs/8.2.0/firebase-app.js");' \
         'importScripts("https://www.gstatic.com/firebasejs/8.2.0/firebase-messaging.js"); ' \
         'var firebaseConfig = {' \
         '        apiKey: "AIzaSyA5QXTBDrkkt6RKDiEJlz2xVjq_YAL7Jww",' \
         '        authDomain: "ludo-27977.firebaseapp.com",' \
         '        databaseURL: "https://ludo-27977-default-rtdb.firebaseio.com",' \
         '        projectId: "ludo-27977",' \
         '        storageBucket: "ludo-27977.appspot.com",' \
         '        messagingSenderId: "773216686826",' \
         '        appId: "1:773216686826:web:2c86813e6a5a284914bd93",' \
         '        measurementId: "G-D84371JPYJ"' \
         ' };' \
         'firebase.initializeApp(firebaseConfig);' \
         'const messaging=firebase.messaging();' \
         'messaging.setBackgroundMessageHandler(function (payload) {' \
         '    console.log(payload);' \
         '    const notification=JSON.parse(payload);' \
         '    const notificationOption={' \
         '        body:notification.body,' \
         '        icon:notification.icon' \
         '    };' \
         '    return self.registration.showNotification(payload.notification.title,notificationOption);' \
         '});'

    return HttpResponse(data,content_type="text/javascript")


def login(request):
    userObj = SessionHandler().verifyMainUserSession(request, sessionFrom='cookies')
    if userObj:
        return redirect('admin/dashboard')
    else:
        # Assuming you have a template named 'login.html'
        return render(request, 'admin/login.html', {
        'recaptcha_site_key': settings.RECAPTCHA_SITE_KEY
        })
        # return render(request, 'login.html')


def get_tokens_for_user(user):
    # Create a new RefreshToken
    refresh = RefreshToken()

    # Encode the user information in the token
    refresh['user_id'] = user.id
    refresh['username'] = user.username  # Include any additional user information you need

    # Access and refresh tokens can be retrieved as follows
    access_token = refresh.access_token
    refresh_token = str(refresh)

    return {
        'access': str(access_token),
        'refresh': refresh_token,
    }

# registration api
class UserRegistrationView(APIView):

    def post(self, request, format=None):
      
        try:
            # import pdb;pdb.set_trace();
            userObj = SessionHandler().verifyMainUserSession(request)
            if not userObj:
                return Response("Authentication Error.", status=status.HTTP_401_UNAUTHORIZED)


            email = request.data.get('email')
            mobile = request.data.get('user_mobile')
            username = request.data.get('username')
            password = Utility().decryptRSAString(request.data.get('password'))
            password2 = Utility().decryptRSAString(request.data.get('password2'))
            
            serializer_data = {
                'user_firstname':request.data.get('user_firstname'),
                'user_lastname':request.data.get('user_lastname'),
                'user_desg':request.data.get('user_desg'),
                'user_mobile':request.data.get('user_mobile'),
                'user_type':request.data.get('user_type'),
                'username': request.data.get('username'),
                'email': request.data.get('email'),
                'password': password,
                'password2': password2,
            }

            # Check if email already exists
            if User.objects.filter(email=email).exists():
                return Response({'status': ResStatus.error.value, 'message': 'Email already exists. Please try another email.'}, status=status.HTTP_400_BAD_REQUEST)

            # Check if mobile number already exists
            if User.objects.filter(user_mobile=mobile).exists():
                return Response({'status': ResStatus.error.value, 'message': 'Mobile number already exists. Please try another mobile number.'}, status=status.HTTP_400_BAD_REQUEST)

            if User.objects.filter(username=username).exists():
                return Response({'status': ResStatus.error.value, 'message': 'Username already exists. Please try another Username.'}, status=status.HTTP_400_BAD_REQUEST)
            
            # import pdb;pdb.set_trace();
            # check email mobile,user validations
            serializer = UserRegistrationSerializer(data=serializer_data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            
            # Retrieve the ID of the newly created user
            user_id = user.id
            UserConsoleOptions.objects.filter(usco_user_id=user_id).delete()
            
            options_list = json.loads(request.data.get("optionsList", "[]"))

            for copt_id in options_list:
                # Ensure copt_id is converted to an integer
                copt_id = int(copt_id)
                UserConsoleOptions.objects.create(usco_user_id=user_id, usco_copt_id=copt_id)

  
            # token = get_tokens_for_user(user)
            return Response({'status': ResStatus.success.value,
                            'message': 'Registered successfully.',
                            # 'token':token,
                            'user_id': user_id}, status=status.HTTP_201_CREATED)

        except Exception as err:
            # Handle specific exceptions, if needed
            return Response({'status': ResStatus.error.value,'message': 'Unable to register User.', 'devMsg': str(err)}, status=status.HTTP_400_BAD_REQUEST)


    def put(self, request, format=None):
        try:
            
            # Verify user session
            userObj = SessionHandler().verifyMainUserSession(request)
            if not userObj:
                return Response("Authentication Error.", status=status.HTTP_401_UNAUTHORIZED)

            # Extract user ID from the request payload
            user_id = request.data.get('id')

            # Retrieve user instance
            user = User.objects.get(id=user_id)

            # Extract data from request payload
            email = request.data.get('email')
            mobile = request.data.get('user_mobile')
            username = request.data.get('username')
            password = request.data.get('password')  # Password from request data

            # Check if email already exists for another user
            if User.objects.filter(email=email).exclude(id=user_id).exists():
                return Response({'status': ResStatus.error.value, 'message': 'Email already exists. Please try another email.'}, status=status.HTTP_400_BAD_REQUEST)

            # Check if mobile number already exists for another user
            if User.objects.filter(user_mobile=mobile).exclude(id=user_id).exists():
                return Response({'status': ResStatus.error.value, 'message': 'Mobile number already exists. Please try another mobile number.'}, status=status.HTTP_400_BAD_REQUEST)

            # Check if username already exists for another user
            if User.objects.filter(username=username).exclude(id=user_id).exists():
                return Response({'status': ResStatus.error.value, 'message': 'Username already exists. Please try another Username.'}, status=status.HTTP_400_BAD_REQUEST)

            # Update user details without hashing password if not provided
            serializer = UserRegistrationSerializer(instance=user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()

            # Update password if provided
            if password:
                user.set_password(password)
                user.save()

            # Update user console options
            # import pdb;pdb.set_trace();
            UserConsoleOptions.objects.filter(usco_user=user).delete()
            options_list = json.loads(request.data.get("optionsList", "[]"))
            for copt_id in options_list:
                # print("Duplicate user console options: user={}, copt_id={}".format(user, copt_id))
                # if not UserConsoleOptions.objects.filter(usco_user=user, usco_copt_id=copt_id).exists():
                UserConsoleOptions.objects.create(usco_user=user, usco_copt_id=copt_id)

                # UserConsoleOptions.objects.create(usco_user=user, usco_copt_id=copt_id)

            return Response({'status': ResStatus.success.value, 'message': 'User details updated successfully.'})

        except Exception as err:
            # Handle specific exceptions, if needed
            return Response({'status': ResStatus.error.value, 'message': 'Unable to update user details.', 'devMsg': str(err)}, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, format=None):
        try:
            # Extract user ID from request data
            user_id = request.data.get("id")
            # Retrieve the user instance
            user = User.objects.get(id=user_id)
            # Set user_status to 'DL' to mark the user as deleted
            user.user_status = 'DL'
            user.save()
            
            return Response({
                'status': ResStatus.success.value,
                'message': 'User deleted successfully.'
            })
        except User.DoesNotExist:
            return Response({'status': ResStatus.error.value, 'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as err:
            return Response({'status': ResStatus.error.value, 'message': 'Unable to delete User.', 'devMsg': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    # def patch(self, request, subRoute=None, subdomain=None):
    #         # Verify user session
    #         userObj = self.sessionHandler.verifyUserSession(request)
            
    #         if not userObj:
    #             return Response("Authentication Error.", status=status.HTTP_401_UNAUTHORIZED)
        
    #         if subRoute == "resetPwd":
    #             try:
    #                 user_id = payload.get("id")
    #                 password = self.utility.decryptRSAString(payload.get("password"))
    #                 password = self.utility.hash_pass(password)

    #                 user = User.objects.get(id=user_id)
    #                 user.user_pwd = password
    #                 user.user_lupdate = timezone.now()
    #                 user.user_luuser_id = puserId
    #                 user.save()

    #                 return {
    #                     'status': 'success',
    #                     'message': 'User password reset successfully.'
    #                 }
    #             except Exception as err:
    #                 self.log.error("users_service reset_user_pwd exception: " + str(err))
    #                 return {
    #                     'status': 'error',
    #                     'message': 'Unable to reset user password.',
    #                     'devMsg': str(err)
    #                 }
          
    #         else:
    #             # status logic write
    #             return 

# reset view
class ResetPasswordView(APIView):
    def patch(self, request):
        try:
            user_id = request.data.get("id")
            decrypted_password = Utility().decryptRSAString(request.data.get('password'))

            user = User.objects.get(id=user_id)
            user.set_password(decrypted_password)
            user.save()

            return Response({
                'status': ResStatus.success.value,
                'message': 'User password reset successfully.'
            }, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({
                'status': ResStatus.error.value,
                'message': 'User not found.'
            }, status=status.HTTP_404_NOT_FOUND)

        except Exception as err:
            return Response({
                'status': ResStatus.error.value,
                'message': 'Unable to reset user password.',
                'devMsg': str(err)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# change status
class ChangeUserStatusView(APIView):
    def patch(self, request):
        try:
            user_id = request.data.get("id")
            new_status = request.data.get("status")

            user = User.objects.get(id=user_id)

      
            user.user_status = new_status
            user.save()

            return Response({
                'status': ResStatus.success.value,
                'message': 'User status updated successfully.'
            }, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({
                'status': ResStatus.error.value,
                'message': 'User not found.'
            }, status=status.HTTP_404_NOT_FOUND)

        except Exception as err:
            return Response({
                'status': ResStatus.error.value,
                'message': 'Unable to update user status.',
                'devMsg': str(err)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# login api
class UserLoginView(APIView):
    def post(self, request, format=None):
        try:
            
            decrypted_password = Utility().decryptRSAString(request.data.get('password'))
            serializer_data = {
                'username': request.data.get('username'),
                'password': decrypted_password,
            }

            serializer = UserLoginSerializer(data=serializer_data)
            serializer.is_valid(raise_exception=True)

            username = serializer.validated_data.get('username')
            # email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')

            # Check if either username or email is provided
            if username:
                user = authenticate(username=username, password=password)
            # elif email:
            #     user = authenticate(email=email, password=password)
            else:
                return Response({'message': 'Username or email must be provided.', 'status': ResStatus.error.value},
                                status=status.HTTP_400_BAD_REQUEST)

            if user is not None:
                 # Update the user's web_fcm_token
                web_fcm_token =  request.data.get('web_fcm_token')
                user.user_fcm_token = web_fcm_token
                user.save()
                
                token = get_tokens_for_user(user)
                jwttoken  = token['access']
                
                hash_password = Utility().hash_pass(decrypted_password)
                sessiontoken = Utility().encryptToRSAString(json.dumps({'username': user.username, 'password': hash_password, 'id': user.id}))
            
                # Get all user data
                user_data = {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'user_desc': user.user_desc,  # Add other fields as needed,
                    'user_type':user.user_type,
                    'sessiontoken': jwttoken
                    # Add other user fields as needed
                }
                # Your authentication logic goes here
                return Response({'status': ResStatus.success.value,
                                 'message': 'Login Success',
                                 'token':sessiontoken,
                                 'user': user_data}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Invalid password or Invalid username/email. Please try again.',
                                 'status': ResStatus.error.value
                                }, status=status.HTTP_200_OK)

        except Exception as err:
            # Handle specific exceptions, if needed
            return Response({'status': ResStatus.error.value, 'message': 'Unable to Login User.', 'devMsg': str(err)},
                            status=status.HTTP_400_BAD_REQUEST)

# log out api
class UserLogoutView(APIView):
    def delete(self, request, format=None):
        # import pdb;pdb.set_trace();
        try:
            return Response({
                'status': ResStatus.success.value,
                'message': 'Logout is successfull'
            }, status=status.HTTP_200_OK)
    
        except Exception as err:
            # Handle specific exceptions, if needed
            return Response({'status': ResStatus.error.value, 'message': 'Unable to Log out', 'devMsg': str(err)},
                            status=status.HTTP_400_BAD_REQUEST)

# profile details
class UserProfileView(APIView):
#   renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  def get(self, request, format=None):
      try:
          serializer = UserProfileSerializer(request.user)
          return Response({'status': ResStatus.success.value,
                            'message': 'Login Success',
                            'user_obj': serializer.data}, status=status.HTTP_200_OK)

      except Exception as err:
            # Handle specific exceptions, if needed
            return Response({'status': ResStatus.error.value, 'message': 'Unable to profiel Details.', 'devMsg': str(err)},
                            status=status.HTTP_400_BAD_REQUEST)
    


    
