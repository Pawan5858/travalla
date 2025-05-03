from django.urls import path
from .import views
from .views import *

urlpatterns = [
    path('appinstallations/',views.appInstallations,name='appinstallations'),
    path('appinstallations/<str:subRoute>/', appInstallationsAPIViewContoller.as_view(), name='users')
]
