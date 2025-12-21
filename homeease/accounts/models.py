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
    
    # Make fields optional with null=True, blank=True for superuser creation
    phone_numberr = models.IntegerField(null=True, blank=True)
    
    # Override first_name and last_name to make them required
    first_name = models. CharField(max_length=150, blank=True)  # Changed to blank=True
    last_name = models.CharField(max_length=150, blank=True)   # Changed to blank=True
    
    # Email is required (override default)
    email = models.EmailField(unique=True, blank=True)  # Changed to blank=True
    
    address = models.TextField(max_length=255, blank=True, null=True)  # Changed
    
    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        blank=True,  # Changed
        null=True    # Added
    )
    
    # Metadata
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