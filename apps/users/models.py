from django.db import models


class Customerusers(models.Model):
    cusr_id = models.AutoField(primary_key=True)
    cusr_full_name = models.CharField(max_length=100, null=True)
    cusr_age = models.IntegerField(null=True, blank=True)
    cusr_email = models.CharField(max_length=255, unique=True, null=False)  # login use
    cusr_password_hash = models.CharField(max_length=255, null=False)
    cusr_profile_image = models.CharField(max_length=255,null=True, blank=True)
    cusr_mobile = models.CharField(max_length=10, null=True, blank=True)
    # cust_type = models.CharField(max_length=20, choices=[('TravelGuideSeeker', 'TravelGuideSeeker'), ('TravelBuddy', 'TravelBuddy')], null=False)
    cusr_is_verified = models.CharField(max_length=1, null=False, default='N')
    cusr_created_at = models.DateTimeField(auto_now_add=True)
    cusr_fcm_token = models.CharField(max_length=500, blank=True, null=True)
    cusr_last_login_timestamp = models.DateTimeField(auto_now_add=True)
    cusr_status = models.CharField(max_length=2, null=False, default='AC')
    cust_otp = models.CharField(max_length=4, blank=True, null=True)   # ofter change its unquie
    
    class Meta:
        db_table = 'customers_users'
        
        
class OTP(models.Model):
    user = models.ForeignKey(Customerusers, on_delete=models.CASCADE ,null=True, blank=True)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'user_otps'
        
        


