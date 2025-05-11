from django.shortcuts import render
from apps.accounts.side_menu import SideMenu
from apps.dashboard.views import *
from apps.utils.utility import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from apps.security.serializers import *
import json
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.utils.timezone import make_aware

import logging
import logging.config
from django.conf import settings
logger = logging.getLogger(__name__)


def users(request,subdomain=None):
    side_menu = SideMenu()
    menu_list = side_menu.currentMenu(request)
    adminPreferencesList = Utility().get_preferences_list(UserType.ADMN.value)
    operatorPreferencesList = Utility().get_preferences_list(UserType.OPTR.value)
   

    pageData = {
        'page_link': 'security',
        'sub_link' : 'users',
        'currentMenu': menu_list,
        'adminPreferencesList': adminPreferencesList,
        'operatorPreferencesList':operatorPreferencesList,
        'admin_console': 'MAIN_ADMIN' 
    }

    # return render(request, 'logistic_operators/logistic_operators.html', {'pageData': pageData})
    return sendResponseScreen(request, subdomain, 'admin/users.html', pageData)


def permissions(request,subdomain=None):
    side_menu = SideMenu()
    menu_list = side_menu.currentMenu(request)
 
   

    pageData = {
        'page_link': 'security',
        'sub_link' : 'permissions',
        'currentMenu': menu_list,
      
        'admin_console': 'MAIN_ADMIN' 
    }

    # return render(request, 'logistic_operators/logistic_operators.html', {'pageData': pageData})
    return sendResponseScreen(request, subdomain, 'commingSoon.html', pageData)


def roles(request,subdomain=None):
    side_menu = SideMenu()
    menu_list = side_menu.currentMenu(request)
 
   

    pageData = {
        'page_link': 'security',
        'sub_link' : 'roles',
        'currentMenu': menu_list,
      
        'admin_console': 'MAIN_ADMIN' 
    }

    # return render(request, 'logistic_operators/logistic_operators.html', {'pageData': pageData})
    return sendResponseScreen(request, subdomain, 'commingSoon.html', pageData)









class UsersTableDataView(APIView):
    serializer_class = UserSerializer

    def post(self, request):
        try:
            # import pdb;pdb.set_trace();
            ser_fname = request.data.get('columns[0][search][value]')
            ser_lname = request.data.get('columns[1][search][value]')
            ser_username = request.data.get('columns[2][search][value]')
            ser_desg = request.data.get('columns[3][search][value]')
            ser_date_from = request.data.get('columns[4][search][value]')
            ser_date_to = request.data.get('columns[5][search][value]')
            ser_status = request.data.get('columns[6][search][value]')


            ser_email = request.data.get('columns[7][search][value]')
            ser_mobile = request.data.get('columns[8][search][value]')
            ser_type = request.data.get('columns[9][search][value]')
           
            ser_start = int(request.data.get('start', 0))
            ser_length = int(request.data.get('length', 10))

            ser_order_colindx = request.data.get('order[0][column]')
            ser_order_colname = request.data.get(f'columns[{ser_order_colindx}][data]')
            ser_order_type = request.data.get('order[0][dir]')

            # queryset = User.objects.exclude(id=1, user_status='DL')
            exclude_condition = Q(id=1)
            exclude_condition |= Q(user_status='DL')

            queryset = User.objects.exclude(exclude_condition)
            
            # mobile_number = '8106505803'
            # msg = Utility().composeSMSText()
            # sms_send = Utility().send_textlocal_sms()

            # print(sms_send)

            if ser_fname:
                queryset = queryset.filter(user_firstname__icontains=ser_fname)

            if ser_lname:
                queryset = queryset.filter(user_lastname__icontains=ser_lname)
            
            if ser_username:
                queryset = queryset.filter(username__icontains=ser_username)  #
                # queryset = queryset.filter(user_username__icontains=ser_username)
            
            if ser_desg:
                queryset = queryset.filter(user_desg__icontains=ser_desg)

            if ser_date_from:
                from_date = datetime.strptime(ser_date_from, "%d-%m-%Y")
                queryset = queryset.filter(created_at__gte=from_date)
        

            if ser_date_to:
                to_date = datetime.strptime(ser_date_to, "%d-%m-%Y")
                to_date = make_aware(datetime.combine(to_date, datetime.max.time()))
                queryset = queryset.filter(created_at__lte=to_date)
            
            if ser_email:
                queryset = queryset.filter(user_email__icontains=ser_email)
            if ser_mobile:
                queryset = queryset.filter(user_mobile__icontains=ser_mobile)
            if ser_type:
                queryset = queryset.filter(user_type=ser_type)
            if ser_status:
                queryset = queryset.filter(user_status=ser_status)

   
            total_count = User.objects.exclude(exclude_condition).count()
            filtered_count = queryset.count()

            if ser_order_colindx:
                ordering_col = ser_order_colname
                if ser_order_type == 'asc':
                    ordering_col = f"-{ordering_col}"
                queryset = queryset.order_by(ordering_col)

            queryset = queryset[ser_start:ser_start + ser_length]

            serializer = self.serializer_class(queryset, many=True)

            result_dict = []
            for user_data in serializer.data:
                user_id = user_data['id']
                user_instance = User.objects.get(id=user_id)
                enabled_opts = UserConsoleOptions.objects.filter(usco_user=user_instance).count()
                options = UserConsoleOptions.objects.filter(usco_user=user_instance).values_list('usco_copt', flat=True)
                total_opts = ConsoleOption.objects.filter(copt_status='AC').count()
               

                user_data.update({
                    'enabled_opts': enabled_opts,
                    'options': list(options),
                    'total_opts': total_opts
                })

                result_dict.append(user_data)

            return Response({
                'recordsFiltered': filtered_count,
                'recordsTotal': total_count,
                'draw': request.data.get('draw', 1),
                'data': result_dict
            })

        except Exception as e:
            logger.error('An error occurred in UsersTableDataView: %s', str(e), exc_info=True)
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

