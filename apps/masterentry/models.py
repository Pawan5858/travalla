from django.db import models
# Create your models here.

class Languages(models.Model):
    lang_id = models.AutoField(primary_key=True)
    lang_name = models.CharField(max_length=50, unique=True, null=False)
    lang_ludate = models.DateTimeField(auto_now=True)  
    lang_status = models.CharField(max_length=2, choices=[('AC', 'Active'), ('NA', 'Not Active')], default='AC')

    class Meta:
        db_table = 'languages'



class Skills(models.Model):
    skil_id = models.AutoField(primary_key=True)
    skil_name = models.CharField(max_length=50, unique=True, null=False)
    skil_ludate = models.DateTimeField(auto_now=True)  
    skil_status = models.CharField(max_length=2, choices=[('AC', 'Active'), ('NA', 'Not Active')], default='AC')
    class Meta:
        db_table = 'skills'
        
class DocumentTypes(models.Model):
    doct_id = models.AutoField(primary_key=True)
    doct_name = models.CharField(max_length=50, unique=True, null=False)
    doct_code = models.CharField(max_length=50, unique=True, null=False)
    doct_ludate = models.DateTimeField(auto_now=True)  
    doct_status = models.CharField(max_length=2, choices=[('AC', 'Active'), ('NA', 'Not Active')], default='AC')
    class Meta:
        db_table = 'document_types'
        
        
class GuideTypes(models.Model):
    gudt_id = models.AutoField(primary_key=True)
    gudt_name = models.CharField(max_length=50, unique=True, null=False)
    gudt_code = models.CharField(max_length=50, unique=True, null=False)
    gudt_ludate = models.DateTimeField(auto_now=True)  
    gudt_status = models.CharField(max_length=2, choices=[('AC', 'Active'), ('NA', 'Not Active')], default='AC')
    class Meta:
        db_table = 'guide_types'
        
        
        
     
        
        
        
        
        
       




