from apps.utils.utility import *
from apps.utils.session_handler import *
from apps.security.models import *

class SideMenu:
    @staticmethod
    def currentMenu(request):
        try:
         
            userObj = SessionHandler().verifyMainUserSession(request, sessionFrom='cookies')
    
            if not userObj:
                return None
            
            if userObj['user_type'] == UserType.ADMN.value:

                menu_list = [
                    {
                        'code': 'DASHBOARD',
                        'name': 'Dashboard',
                        'link': 'dashboard',
                        'icon': 'dashboard',
                    },
                    {
                        'code': 'ALERTS',
                        'name': 'Alerts',
                        'link': 'alerts',
                        'icon': 'alerts',
                        'subMenu': [
                            {
                                'code': 'IMPORTANTALERTS',
                                'name': 'Important Alerts',
                                'link': 'importantalerts'
                            }
                        ]
                    },
                    {
                        'code': 'CUSTOMERS',
                        'name': 'Customers',
                        'link': 'customers' 
                    },
                    {
                        'code': 'REGISTEREDGUIDES',
                        'name': 'Registered Guides',
                        'link': 'registerguides' 
                    },
                    {
                        'code': 'GUIDES',
                        'name': 'Guides',
                        'link': 'guides' 
                    },
                    {
                        'code': 'TRAVELLAGENCY',
                        'name': 'Travell Agency',
                        'link': 'travellagency' 
                    },
                    {
                        'code': 'MASTERENTRY',
                        'name': 'Master Entry',
                        'link': 'masterEntry',
                        'subMenu': [
                            {
                                'code': 'TOURPACKAGES',
                                'name': 'Tour Packages',
                                'link': 'tourpackages'
                            }
                            ]
                    },
                    {
                        'code': 'PAYMENTS',
                        'name': 'Payments',
                        'link': 'payments',
                        'icon': 'payments',
                        'subMenu': [
                            {
                                'code': 'SETTLEMENTREQUESTS',
                                'name': 'Settlement Requests',
                                'link': 'settlementrequests'
                            },
                            {
                                'code': 'SETTLEMENTSPAYMENTS',
                                'name': 'Settlements Payments',
                                'link': 'settlementspayments'
                            }
                        ]
                    },
                    
                    {
                        'code': 'REPORTS',
                        'name': 'Reports',
                        'link': 'reports',
                        'icon': 'reports',
                        'subMenu': [
                            {
                                'code': 'DAILYREPORTS',
                                'name': 'Daily Reports',
                                'link': 'dailyreports'
                            }
                        ]
                    },
                    {
                        'code': 'SECURITY',
                        'name': 'Security',
                        'link': 'security',
                        'icon': 'settings',
                        'subMenu': [
                            {
                                'code': 'USERS',
                                'name': 'Users',
                                'link': 'users'
                            },
                            {
                                'code': 'APPROVALS',
                                'name': 'Approvals',
                                'link': 'approvals'
                            },
                        ]
                    },
                    {
                        'code': 'APPINSTALLATIONS',
                        'name': 'App Installations',
                        'link': 'appinstallations' 
                    },      
                ]
           
            else:
                
                menu_list = [
                    {
                        'code': 'DASHBOARD',
                        'name': 'Dashboard',
                        'link': 'dashboard',
                        'icon': 'dashboard',
                    },
                    {
                        'code': 'ALERTS',
                        'name': 'Alerts',
                        'link': 'alerts',
                        'icon': 'alerts',
                        'subMenu': [
                            {
                                'code': 'IMPORTANTALERTS',
                                'name': 'Important Alerts',
                                'link': 'importantalerts'
                            }
                        ]
                    },
                    {
                        'code': 'CUSTOMERS',
                        'name': 'Customers',
                        'link': 'customers' 
                    },
                    {
                        'code': 'REGISTEREDGUIDES',
                        'name': 'Registered Guides',
                        'link': 'registerguides' 
                    },
                    {
                        'code': 'GUIDES',
                        'name': 'Guides',
                        'link': 'guides' 
                    },
                    {
                        'code': 'TRAVELLAGENCY',
                        'name': 'Travell Agency',
                        'link': 'travellagency' 
                    },
                    {
                        'code': 'MASTERENTRY',
                        'name': 'Master Entry',
                        'link': 'masterEntry',
                        'subMenu': [
                            {
                                'code': 'TOURPACKAGES',
                                'name': 'Tour Packages',
                                'link': 'tourpackages'
                            }
                            ]
                    },
                    {
                        'code': 'PAYMENTS',
                        'name': 'Payments',
                        'link': 'payments',
                        'icon': 'payments',
                        'subMenu': [
                            {
                                'code': 'SETTLEMENTREQUESTS',
                                'name': 'Settlement Requests',
                                'link': 'settlementrequests'
                            },
                            {
                                'code': 'SETTLEMENTSPAYMENTS',
                                'name': 'Settlements Payments',
                                'link': 'settlementspayments'
                            }
                        ]
                    },
                    
                    {
                        'code': 'REPORTS',
                        'name': 'Reports',
                        'link': 'reports',
                        'icon': 'reports',
                        'subMenu': [
                            {
                                'code': 'DAILYREPORTS',
                                'name': 'Daily Reports',
                                'link': 'dailyreports'
                            }
                        ]
                    },
                    {
                        'code': 'SECURITY',
                        'name': 'Security',
                        'link': 'security',
                        'icon': 'settings',
                        'subMenu': [
                            {
                                'code': 'USERS',
                                'name': 'Users',
                                'link': 'users'
                            },
                            {
                                'code': 'APPROVALS',
                                'name': 'Approvals',
                                'link': 'approvals'
                            },
                        ]
                    },
                    {
                        'code': 'APPINSTALLATIONS',
                        'name': 'App Installations',
                        'link': 'appinstallations' 
                    },      
                ]
           
            user_id = userObj['user_id']

            # Fetch user's console options using Django ORM
            user_pref_data = UserConsoleOptions.objects.filter(usco_user_id=user_id).values_list('usco_copt__copt_code', flat=True)
            
          
            url_lastpath = request.path.split("/")[-2]
            has_permission_for_curr_page = True
            has_curr_page = False
            
            # Assuming menuList is a list similar to what you have in your original code
            for obj in menu_list:
                if obj.get('subMenu'):
                    for sub_menu_obj in obj['subMenu']:
                        if url_lastpath == sub_menu_obj['link']:
                            has_curr_page = True
                        if sub_menu_obj['code'] not in user_pref_data:
                            sub_menu_obj['code'] = None
                            if url_lastpath == sub_menu_obj['link']:
                                has_permission_for_curr_page = False
                    obj['subMenu'] = [sub_menu for sub_menu in obj['subMenu'] if sub_menu['code'] is not None]
                    obj['code'] = obj['code'] if len(obj['subMenu']) > 0 else None
                else:
                    if url_lastpath == obj['link']:
                        has_curr_page = True
                    if obj['code'] not in user_pref_data:
                        obj['code'] = None
                        if url_lastpath == obj['link']:
                            has_permission_for_curr_page = False

            menu_list = [obj for obj in menu_list if obj['code'] is not None]

            if not has_curr_page:
                has_permission_for_curr_page = False
            
            print("menu_list", menu_list)  
            # return menu_list
            return {
                'menuList': menu_list,
                'hasPermissionForCurrPage': has_permission_for_curr_page
            }

        except Exception as e:
            # logger.error(f"An error occurred in generate_menu: {e}")
            return []
