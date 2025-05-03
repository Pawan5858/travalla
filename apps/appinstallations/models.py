from django.db import models

# Create your models here.
class AppInstallation(models.Model):
    appi_id = models.AutoField(primary_key=True)
    appi_idate = models.DateTimeField(auto_now_add=True)  
    appi_catg = models.CharField(max_length=100, blank=True, null=True)  
    appi_uniqid = models.CharField(max_length=255, unique=True)  
    appi_device_act = models.CharField(max_length=255, blank=True, null=True)  
    appi_appversion = models.CharField(max_length=50, blank=True, null=True)  
    appi_devicetype = models.CharField(max_length=100, blank=True, null=True)  
    appi_devicemodel = models.CharField(max_length=100, blank=True, null=True)  
    appi_devicemake = models.CharField(max_length=100, blank=True, null=True)  
    appi_deviceos = models.CharField(max_length=50, blank=True, null=True)  
    appi_deviceosversion = models.CharField(max_length=50, blank=True, null=True)  
    appi_pntoken = models.CharField(max_length=255, blank=True, null=True)  
    
    class Meta:
        db_table = 'app_installations'
