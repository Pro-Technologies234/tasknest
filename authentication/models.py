from django.contrib.auth.models import AbstractUser
from django.db import models
from .manager import CustomUserManager

class CustomUser(AbstractUser):
    username = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female')])
    birthdate = models.DateField(blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['gender']

    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    def _str_(self):
        return self.email

    def save(self, *args, **kwargs):
        if not self.is_superuser:
            self.is_superuser = False
        if not self.is_staff:
            self.is_staff = False
        super(CustomUser, self).save(*args, **kwargs)
