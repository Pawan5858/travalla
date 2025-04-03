from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


# Custom User Manager
class UserManager(BaseUserManager):
    
    def create_user(self, username, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given username, email, and password.
        """
        if not email and not username:
            raise ValueError('User must have an email address or username')

        email = self.normalize_email(email)
        # Set is_admin and is_active if not provided in extra_fields
        extra_fields.setdefault('is_admin', False)
        extra_fields.setdefault('is_active', True)
        user = self.model(
            email=email,
            username=username,
            **extra_fields
        )
        
        user.is_active = True  # Set is_active directly here
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given username, email, and password.
        """
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_admin') is not True:
            raise ValueError('Superuser must have is_admin=True.')

        return self.create_user(username, email, password, **extra_fields)


# Custom User Model
class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True,
    )
    username = models.CharField(
        verbose_name='Username',
        max_length=80,
        unique=True,
    )
    
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Extra fields (add your custom fields here)
    user_firstname = models.CharField(max_length=80, null=True, blank=True)
    user_lastname = models.CharField(max_length=80, null=True, blank=True)
    user_desc = models.CharField(max_length=255, null=True, blank=True)
    user_adate = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    user_status = models.CharField(max_length=4, null=True, blank=True, default='AC')
    user_type = models.CharField(max_length=50, null=True, blank=True)
    user_mobile = models.CharField(max_length=15, null=True, blank=True)
    user_desg = models.CharField(max_length=100, null=True, blank=True)
    user_fcm_token = models.TextField(default=None, null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


# customer registratin model
