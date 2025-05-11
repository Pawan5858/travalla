from django.urls import path
from .import views
from .views import *

urlpatterns = [
    path('appinstallations/',views.appInstallations,name='appinstallations'),
    path('importantalerts/',views.importantalerts,name='importantalerts'),
    path('travellagency/',views.travellagency,name='travellagency'),
    path('dailyreports/',views.dailyreports,name='dailyreports'),
    path('appinstallations/<str:subRoute>/', appInstallationsAPIViewContoller.as_view(), name='users')
]
