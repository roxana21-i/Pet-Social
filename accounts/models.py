from django.db import models
from django.contrib import auth
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill, SmartCrop
from cloudinary.models import CloudinaryField
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # avatar = models.ImageField(upload_to='profile_pics', default='profile_pics/default.jpg')
    avatar = CloudinaryField('image', blank=True, null=True)
    # avatar_thumbnail = ImageSpecField(source='avatar',
    #                                   processors=[ResizeToFill(300,300), SmartCrop(200, 200)],
    #                                   format='JPEG',
    #                                   options={'quality': 80})

    def __str__(self):
        return self.user.username
