from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import ASCIIUsernameValidator
# Create your models here.
class Users(AbstractUser):
    username_valid = ASCIIUsernameValidator()
    username = models.CharField(
        unique=True,
        max_length=30,
        validators=[username_valid]
    )
    
    description = models.CharField(max_length=500, blank=True, default="")
    bio = models.TextField(blank=True, default="")
