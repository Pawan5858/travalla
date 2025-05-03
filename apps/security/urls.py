from django.urls import path
from .import views
from apps.security.views import *

urlpatterns = [
    # web views
    path('users/',views.users,name='users'),
    path('permissions/',views.permissions,name='permissions'),
    path('roles/',views.roles,name='roles'),
    path('users_tabledata/', UsersTableDataView.as_view(), name='users_tabledata'),
]
