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
from apps.masterentry.views import masterEntryAPIViewContoller


def tour_packages(request,subdomain=None):
    side_menu = SideMenu()
    menu_list = side_menu.currentMenu(request)
    pageData = {
        'page_link': 'approvals',
        'currentMenu': menu_list,
        'admin_console': 'MAIN_ADMIN' ,
    }
    pageData['destinations'] = masterEntryAPIViewContoller().destinations()
    return sendResponseScreen(request, subdomain, 'admin/tour_packages.html', pageData)


def sendResponseScreen(request, subdomain, pagePath, pageData):
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

class tourPackageAPIViewContoller(APIView):
    
    def __init__(self):
        self.service = tourPackagesServices()
        self.utility = Utility()
        self.sessionHandler =SessionHandler()
        self.log =logging.getLogger(__name__)
    
    def get(self, request, api_version=None , subRoute=None, subdomain =None):
        if subRoute =='get_all_packages':
            torp_id = request.query_params.get('torp_id', None)
            torp_name = request.query_params.get('torp_name', None)
            if not (torp_id and torp_name):
                self.log.error("Required fields must not be empty for applied contests.")
                return Response("Required fields must not be empty for applied contests.", status=status.HTTP_400_BAD_REQUEST)
            return self.service.get_all_tour_packages(torp_id, torp_name)
        
    def post(self, request, subRoute):
        try:
            
            payload =request.data
            
            if subRoute=='add_tour_package':
                return self.service.add_tour_package(request)
            
            elif subRoute=='packages_tabledata':
                return self.service.packages_tabledata(request)
            
            elif subRoute=='resend-otp':
                if not (payload.get("email")):
                    self.log.error("Required fields must not be empty for login.")
                    return Response("Required fields must not be empty for login.", status=status.HTTP_400_BAD_REQUEST)
                return self.service.resendOTP(request)
            
            elif subRoute=='verify-otp':
                if not (payload.get("email") and payload.get("otp")):
                    self.log.error("Required fields must not be empty for login.")
                    return Response("Required fields must not be empty for login.", status=status.HTTP_400_BAD_REQUEST)
                return self.service.verifyOTP(request)
            
            
        except Exception as err:

            logger.error('user exception: Required fields are empty: %s', str(err), exc_info=True)

            return Response({'status': ResStatus.error.value, 'message': 'user failed with error ' + str(err)}, 
                            status=status.HTTP_400_BAD_REQUEST)
            
    def put(self, request, subRoute):
        try:
            
            payload =request.data
            if subRoute =='add_tour_package':
                return self.service.update_tour_package(payload) 
            
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
                return self.service.change_package_status(payload)  # Ensure partial updates
            
            elif subRoute == 'change_apr_status':
                return self.service.change_apr_status(payload)  # Ensure partial updates    
        except Exception as err:
            logger.error('ordersr updateRazorpayPayment exception: Required fields are empty: %s', 
                        str(err), exc_info=True)

            return Response({'status': ResStatus.error.value, 
                            'message': 'Payment failed with error ' + str(err)}, 
                            status=status.HTTP_400_BAD_REQUEST) 

    