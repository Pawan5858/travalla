from django.urls import path
from .import views
from .views import *

urlpatterns = [
    path('masterentry/<str:subRoute>/', masterEntryAPIViewContoller.as_view(), name='masterentry'),
]