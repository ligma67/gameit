from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator
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

class Game(models.Model):
    name = models.CharField(max_length=50, validators=[MinLengthValidator(4)])
    short_description = models.CharField(max_length=150)
    description = models.CharField(max_length=500)
    image = models.ImageField(default="game_icons/default_icon.png", upload_to="game_icons/")
    is_active = models.BooleanField(default=False)
    
class Rate(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='ratings')
    mark = models.IntegerField(default=10, validators=[
        MinValueValidator(1), MaxValueValidator(10)
    ])
    comment = models.CharField(max_length=255, null=True)