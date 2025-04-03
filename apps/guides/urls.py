from django.urls import path
from .import views
from .views import *

urlpatterns = [
    path('approvals/',views.approvals,name='approvals'),
    path('guides/<str:subRoute>/', guidesAPIViewContoller.as_view(), name='users'),
]