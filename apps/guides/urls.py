from django.urls import path
from .import views
from .views import *

urlpatterns = [
    path('approvals/',views.approvals,name='approvals'),
    path('registerguides/',views.registered_guides,name='guides'),
    path('guides/',views.guides,name='guides'),
    path('guides/<str:subRoute>/', guidesAPIViewContoller.as_view(), name='users')
]
