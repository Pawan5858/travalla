from django.urls import path
from .import views
from .views import *

urlpatterns = [
    path('tourpackages/',views.tour_packages,name='tourpackages'),
    path('tour/<str:subRoute>', tourPackageAPIViewContoller.as_view(), name='tourpackages')
]