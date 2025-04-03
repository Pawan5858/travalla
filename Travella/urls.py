"""Travella URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from apps.accounts.views import *

urlpatterns = [
    path('admin/', admin.site.urls),

    path('firebase-messaging-sw.js',showFirebaseJS,name="show_firebase_js"),
    # accounts
    path('clientAdmin/',include('apps.accounts.urls'),name='accounts'),
    path('',include('apps.accounts.urls'),name='accounts'),
    # security
    path('clientAdmin/',include('apps.security.urls'),name='security'),
    path('api/v1/',include('apps.security.urls'),name='security'),
    # dashboard
    path('clientAdmin/',include('apps.dashboard.urls'),name='dashboard'),
    # reports
    path('clientAdmin/',include('apps.reports.urls'),name='reports'),
    path('api/v1/',include('apps.reports.urls'),name='reports'),
    
    # app installations
    path('clientAdmin/',include('apps.appinstallations.urls'),name='appinstallations'),
    path('api/v1/',include('apps.appinstallations.urls'),name='appinstallations'),
    
    # users
    path('clientAdmin/',include('apps.users.urls'),name='users'),
    path('api/v1/',include('apps.users.urls'),name='users'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




