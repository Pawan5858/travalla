from django.urls import path
from .import views
from apps.accounts.views import *

urlpatterns = [
    path('settings/',views.settings_function,name='settings_function'),
    path('mis-reports/',views.MIS_reports,name='MIS_reports'),   
    path('daily-reports/',views.daily_reports,name='daily_reports'), 
    path('login/',views.login,name='login'),
    path('api/v1/user/', UserRegistrationView.as_view(), name='user'),
    path('api/v1/reset_password/', ResetPasswordView.as_view(), name='reset_password'),
    path('api/v1/change_status/', ChangeUserStatusView.as_view(), name='change_user_status'),
    path('api/v1/login/', UserLoginView.as_view(), name='api_login'),
    path('api/v1/logout/', UserLogoutView.as_view(), name='api_logout'),
    path('api/v1/profile/', UserProfileView.as_view(), name='profile'),
    
    
]