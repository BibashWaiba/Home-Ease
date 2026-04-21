from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Custom User model extending AbstractUser with additional fields
    for registration form
    """
    
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    )
    

    phone_numberr = models.IntegerField(null=True, blank=True)
    
   
    first_name = models. CharField(max_length=150, blank=True) 
    last_name = models.CharField(max_length=150, blank=True)   
    
  
    email = models.EmailField(unique=True, blank=True)  
    
    address = models.TextField(max_length=255, blank=True, null=True)  
    
    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        blank=True,  
        null=True   
    )
    
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.username
    
    def get_full_name(self):
        """Return the first_name plus the last_name, with a space in between."""
        return f"{self.first_name} {self.last_name}".strip()
    
    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

class PasswordResetOTP(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return f"OTP for {self.user.username}"