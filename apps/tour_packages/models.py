from django.db import models
from apps.accounts.models import *
from apps.masterentry.models import Destination

class TourPackage(models.Model):
    
    PACKAGE_TYPES = (
        ('DIRECT', 'Direct Package'),
        ('ITINERARY', 'Itinerary Package'),
    )
    
    torp_id  = models.AutoField(primary_key=True)
    torp_name = models.CharField(max_length=200, null=False, blank=False)
    torp_description = models.TextField(null=True, blank=True)
    torp_image = models.CharField(max_length=250,null=True, blank=True)
    torp_price = models.DecimalField(max_digits=10, decimal_places=2)
    torp_package_type = models.CharField(max_length=10, choices=PACKAGE_TYPES, default='DIRECT')
    torp_duration = models.PositiveIntegerField(null=False, blank=False)  # Duration in days
    torp_destination = models.ForeignKey(Destination, on_delete=models.CASCADE, null=True,blank=True, related_name='primary_packages')
    torp_start_location = models.ForeignKey(Destination, on_delete=models.CASCADE, null=True, blank=True, related_name='start_packages')
    torp_end_destination = models.ForeignKey(Destination, on_delete=models.CASCADE, null=True,blank=True, related_name='end_packages')
    torp_start_date = models.DateField(null=True, blank=True)
    torp_end_date = models.DateField(null=True, blank=True)
    torp_inclusions = models.TextField(null=True, blank=True)
    torp_status = models.TextField(null=True, blank=True, default='AC')
    
    class Meta:
        db_table = 'tour_packages'  
        
        
        
# Itineraries model (optional, included for day-wise plans)
class TourPackageItinerary(models.Model):
    itnr_id =models.AutoField(primary_key=True)
    itnr_package = models.ForeignKey(TourPackage,on_delete=models.CASCADE,null=True,blank=True)
    itnr_day_number = models.PositiveIntegerField(null=False, blank=False)
    itnr_date = models.DateField(null=False, blank=False)
    itnr_activities = models.TextField(null=True, blank=True)
    itnr_location = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = 'tour_package_itineraries'  



