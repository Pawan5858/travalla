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
from apps.accounts.side_menu import SideMenu


def users(request,subdomain=None):
    side_menu = SideMenu()
    menu_list = side_menu.currentMenu(request)
    pageData = {
        'page_link': 'customers',
        'currentMenu': menu_list,
        'admin_console': 'MAIN_ADMIN' ,
    }
    
    return sendResponseScreen(request, subdomain, 'admin/customers.html', pageData)

def approvals(request,subdomain=None):
    side_menu = SideMenu()
    menu_list = side_menu.currentMenu(request)
    pageData = {
        'page_link': 'customers',
        'currentMenu': menu_list,
        'admin_console': 'MAIN_ADMIN' ,
    }
    
    return sendResponseScreen(request, subdomain, 'customers.html', pageData)


def sendResponseScreen(request, subdomain, pagePath, pageData):
    # import pdb;pdb.set_trace();
    if subdomain:
        return render(request, '404.html')
    
    elif not pageData['currentMenu']:
        return redirect('login')
  
    else:
        hasPermissionForCurrPage = pageData['currentMenu']['hasPermissionForCurrPage']
        pageData['currentMenu'] = pageData['currentMenu']['menuList']
        pageData['admin_console'] = AdminConsoleTypes.main_admin.value
        
        if hasPermissionForCurrPage:
            
            return render(request, pagePath, {'pageData': pageData})  # Use 'context' instead of 'pageData'
        else:
            return render(request, 'noPermission.html', {'pageData': pageData})  # Use 'context' instead of 'p


class usersAPIViewContoller(APIView):
    
    def __init__(self):
        self.service = userServices()
        self.utility = Utility()
        self.sessionHandler =SessionHandler()
        self.log =logging.getLogger(__name__)
    
    def get(self, request, api_version=None , subRoute=None, subdomain =None):
        if subRoute =='get_applied_contests':
            source_type = request.query_params.get('source_type', None)
            source_id = request.query_params.get('source_id', None)
            if not (source_type and source_id):
                self.log.error("Required fields must not be empty for applied contests.")
                return Response("Required fields must not be empty for applied contests.", status=status.HTTP_400_BAD_REQUEST)
            return self.service.get_applied_contests(source_type, source_id)
        
        
        
    def post(self, request, subRoute):
        try:
            payload =request.data
            if subRoute=='registration':
                if not (payload.get("email") and payload.get("password")):
                    self.log.error("Required fields must not be empty for registration.")
                    return Response("Required fields must not be empty for registration.", status=status.HTTP_400_BAD_REQUEST)
                return self.service.registerCustomerUser(payload)
            elif subRoute=='verify_otp':
                if not (payload.get("email") and payload.get("otp")):
                    self.log.error("Required fields must not be empty for registration.")
                    return Response("Required fields must not be empty for registration.", status=status.HTTP_400_BAD_REQUEST)
                return self.service.verifyOtp(payload)
            elif subRoute=='resend_otp':
                if not (payload.get("email")):
                    self.log.error("Required fields must not be empty for registration.")
                    return Response("Required fields must not be empty for registration.", status=status.HTTP_400_BAD_REQUEST)
                return self.service.resendOtp(payload)
            
            elif subRoute=='login':
                if not (payload.get("username") and payload.get("password") and 
                    payload.get("fcm_token")):
                    self.log.error("Required fields must not be empty for login.")
                    return Response("Required fields must not be empty for login.", status=status.HTTP_400_BAD_REQUEST)
                return self.service.loginUser(request)
            elif subRoute=='approved' and request.GET.get('datatable') == 'true':
                return self.service.register_customers_table_data(request)
                
            
                
        except Exception as err:

            logger.error('user exception: Required fields are empty: %s', str(err), exc_info=True)

            return Response({'status': ResStatus.error.value, 'message': 'user failed with error ' + str(err)}, 
                            status=status.HTTP_400_BAD_REQUEST)
            
    def put(self, request, subRoute):
        try:
            
            payload =request.data
            if subRoute =='update_account':
                return self.service.update_account(payload) 
            
            elif subRoute =='update_consoleoptions':
                return self.service.update_consoleoptions(payload) 
                
            
        except Exception as err:

            logger.error('ordersr updateRazorpayPayment exception: Required fields are empty: %s', str(err), exc_info=True)

            return Response({'status': ResStatus.error.value, 'message': 'Payment failed with error ' + str(err)}, 
                            status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, subRoute):
        try:
            payload = request.data
            if subRoute == 'change_status':
                return self.service.change_account_status(payload, partial=True)  # Ensure partial updates
                
        except Exception as err:
            logger.error('ordersr updateRazorpayPayment exception: Required fields are empty: %s', 
                        str(err), exc_info=True)

            return Response({'status': ResStatus.error.value, 
                            'message': 'Payment failed with error ' + str(err)}, 
                            status=status.HTTP_400_BAD_REQUEST) 

