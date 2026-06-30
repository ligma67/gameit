from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator
import io
from django.db import models
from django.core.files.base import ContentFile
from PIL import Image
import uuid
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
    site_url_name = models.CharField(max_length=100, unique=True)
    
    short_description = models.CharField(max_length=150)
    description = models.CharField(max_length=500)
    
    icon = models.ImageField(default="game_icons/default_icon.png", upload_to="game_icons/")
    
    game_link = models.URLField(max_length=200, blank=True)
    is_active = models.BooleanField(default=False)
    
    author = models.ForeignKey(Users, on_delete=models.SET_NULL, related_name='games', null=True) # null if something happened with the author
    def save(self, *args, **kwargs):
        if self.icon: # if img for some reason doesnt get compressed by js
           
            img = Image.open(self.icon)
            MAX_SIZE = (300, 300)
            width, height = img.size
            
            img.thumbnail(MAX_SIZE, Image.Resampling.LANCZOS)
            buffer = io.BytesIO()
            img.convert("RGB").save(buffer, format="JPEG", quality=80)
            buffer.seek(0)
            new_filename = f"{uuid.uuid4()}.jpg"
            
            self.icon.field.save_form_data(self, ContentFile(buffer.read(), name=new_filename))
            
        super().save(*args, **kwargs)
    
class Rate(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='ratings')
    mark = models.IntegerField(default=10, validators=[
        MinValueValidator(1), MaxValueValidator(10)
    ])
    comment = models.CharField(max_length=255, null=True) # todo: add datetimes?