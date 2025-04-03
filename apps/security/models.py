from django.db import models
from apps.accounts.models import *

class ConsoleOptionCategory(models.Model):
    STATUS_CHOICES = [
        ('AC', 'Active'),
        ('NA', 'Inactive'),
    ]

    copc_id = models.AutoField(primary_key=True)
    copc_code = models.CharField(max_length=30, unique=True)
    copc_name = models.CharField(max_length=30)
    copc_parent_id = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    copc_status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='AC')
    copc_category = models.CharField(max_length=255) 
    class Meta:
        db_table = 'console_option_categories'
        

class ConsoleOption(models.Model):
    STATUS_CHOICES = [
        ('AC', 'Active'),
        ('NA', 'Inactive'),
    ]

    copt_id = models.AutoField(primary_key=True)
    copt_code = models.CharField(max_length=50, unique=True)
    copt_name = models.CharField(max_length=50)
    copt_status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='AC')
    copt_copc_id = models.ForeignKey(ConsoleOptionCategory, on_delete=models.SET_NULL, null=True, blank=True)
    copt_category = models.CharField(max_length=10, default='ADMN', null=True, blank=True)
    
    class Meta:
        db_table = 'console_options'
        
               
class UserConsoleOptions(models.Model):
    usco_id = models.AutoField(primary_key=True)
    usco_user = models.ForeignKey(User, on_delete=models.CASCADE)
    usco_copt = models.ForeignKey(ConsoleOption, on_delete=models.CASCADE)

    class Meta:
        db_table = 'user_console_options'

        