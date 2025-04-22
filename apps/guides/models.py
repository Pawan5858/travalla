from django.db import models
from apps.masterentry.models import DocumentTypes, GuideTypes, Languages, Skills

class Guides(models.Model):
    gude_id = models.AutoField(primary_key=True)
    gude_full_name = models.CharField(max_length=100, null=False)
    gude_age = models.IntegerField(null=False)
    gude_email = models.CharField(max_length=255, unique=True, null=False)
    gude_mobile = models.CharField(max_length=10, unique=True, null=False)
    gude_password_hash = models.CharField(max_length=255, null=False)
    gude_profile_image = models.CharField(max_length=255, null=False)
    gude_type = models.ForeignKey(GuideTypes, on_delete=models.CASCADE, null=False, blank=True)
    gude_has_car = models.CharField(max_length=2,default='NA', null=False)
    gude_experiance = models.IntegerField(null=False)
    gude_is_verified = models.CharField(max_length=3,default='YTA', null=False)
    gude_fcm_token = models.CharField(max_length=500, null=False)
    gude_created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'guides'
        
class GuideLanguages(models.Model):
    gdln_id = models.AutoField(primary_key=True)
    gdln_gude = models.ForeignKey(Guides, on_delete=models.CASCADE, null=False, blank=True)
    gdln_lang = models.ForeignKey(Languages, on_delete=models.CASCADE, null=False, blank=True)
    
    class Meta:
        db_table = 'guide_languages'
        unique_together = (('gdln_gude', 'gdln_lang'),)  # composite key
        
        
class GuideSkills(models.Model):
    gdsk_id = models.AutoField(primary_key=True)
    gdsk_gude = models.ForeignKey(Guides, on_delete=models.CASCADE, null=False, blank=True)
    gdsk_skill = models.ForeignKey(Skills, on_delete=models.CASCADE, null=False, blank=True)
    
    class Meta:
        db_table = 'guide_skills'
        unique_together = (('gdsk_gude', 'gdsk_skill'),)  # Composite primary key equivalent 
        
        
class GuideDocuments(models.Model):
    gddc_id = models.AutoField(primary_key=True)
    gddc_gude = models.ForeignKey(Guides, on_delete=models.CASCADE, null=False, blank=True)
    gddc_doct = models.ForeignKey(DocumentTypes, on_delete=models.CASCADE, null=False, blank=True)
    gddc_doc_file = models.CharField(max_length=255, null=False)  # File path or URL
    Equipmentgddc_uploaded_at = models.DateTimeField(auto_now_add=True)
    gddc_status = models.CharField(max_length=4, default='AC')  # Active or any other status

    class Meta:
        db_table = 'guide_documents'
        unique_together = (('gddc_gude', 'gddc_doct'),)
