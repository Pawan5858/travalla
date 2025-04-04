from django.shortcuts import render
from apps.accounts.side_menu import SideMenu
from apps.utils.enums import *
from django.shortcuts import redirect

def dashboard(request,subdomain=None):
    side_menu = SideMenu()
    menu_list = side_menu.currentMenu(request)

    pageData = {
        'page_link': 'dashboard',
        'currentMenu': menu_list,
        'admin_console': 'MAIN_ADMIN'  # Replace with your logic
    }
    
    # return render(request, 'dashboard.html', {'pageData': pageData})
    return sendResponseScreen(request,subdomain, 'admin/dashboard.html', pageData)



def sendResponseScreen(request, subdomain, pagePath, pageData):
    # import pdb;pdb.set_trace();
    if subdomain:
        return render(request, '404.html')
    
    elif not pageData['currentMenu']:
        return redirect('admin/login')
  
    else:
        hasPermissionForCurrPage = pageData['currentMenu']['hasPermissionForCurrPage']
        pageData['currentMenu'] = pageData['currentMenu']['menuList']
        pageData['admin_console'] = AdminConsoleTypes.main_admin.value
        
        if hasPermissionForCurrPage:
            
            return render(request, pagePath, {'pageData': pageData})  # Use 'context' instead of 'pageData'
        else:
            return render(request, 'noPermission.html', {'pageData': pageData})  # Use 'context' instead of 'p
