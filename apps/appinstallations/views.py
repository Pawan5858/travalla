from django.shortcuts import render
from apps.accounts.side_menu import SideMenu
from apps.utils.enums import *
from django.shortcuts import redirect
from apps.utils.enums import *
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.utils.utility import *
from apps.utils.session_handler import *
from .services import *



def appInstallations(request,subdomain=None):
    side_menu = SideMenu()
    menu_list = side_menu.currentMenu(request)

    pageData = {
        'page_link': 'appinstallations',
        'currentMenu': menu_list,
        'admin_console': 'MAIN_ADMIN'  # Replace with your logic
    }
    
    # return render(request, 'dashboard.html', {'pageData': pageData})
    return sendResponseScreen(request,subdomain, 'admin/app_installations.html', pageData)



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

class appInstallationsAPIViewContoller(APIView):
    
    def __init__(self):
        self.service = appInstallationsServices()
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
            if subRoute=='app_installation':
                if not (payload.get("appi_uniqid") and payload.get("") and 
                    payload.get("email")):
                    self.log.error("Required fields must not be empty for registration.")
                    return Response("Required fields must not be empty for registration.", status=status.HTTP_400_BAD_REQUEST)
                return self.service.app_installation(payload)
            
            elif(subRoute=='app_installation_table_data'):
                return self.service.app_installation_table_data(request)
            
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
            elif subRoute == 'change_apr_status':
                return self.service.change_apr_status(payload)  # Ensure partial updates    
        except Exception as err:
            logger.error('ordersr updateRazorpayPayment exception: Required fields are empty: %s', 
                        str(err), exc_info=True)

            return Response({'status': ResStatus.error.value, 
                            'message': 'Payment failed with error ' + str(err)}, 
                            status=status.HTTP_400_BAD_REQUEST) 




