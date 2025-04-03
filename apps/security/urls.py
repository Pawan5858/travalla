from django.urls import path
from .import views
from apps.security.views import *

urlpatterns = [
    # web views
    path('users/',views.users,name='users'),
    path('permissions/',views.permissions,name='permissions'),
    path('roles/',views.roles,name='roles'),




    
    path('users_tabledata/', UsersTableDataView.as_view(), name='users_tabledata'),
    
    # api views
    # path('logistic_operators/', LogisticOperatorsAPIView.as_view(), name='logistic_operator'),
    # path('logistic_operators/<int:lgop_id>/', LogisticOperatorsAPIView.as_view(), name='logistic_operator_id'),
    # path('logistic_operators_table_data/', LogisticOperatorsTableData.as_view(), name='logistic_operator_table_data'),
    # path('vehicle-type-table-data/', VehicleTypeTableData.as_view(), name='vehicle_type_table_data'),
    
]