from django.urls import path
from .import views
from .views import *

urlpatterns = [
    path('users/<str:subRoute>/', usersAPIViewContoller.as_view(), name='users'),
]