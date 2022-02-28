from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils import timezone
from imagekit.models import ImageSpecField
from imagekit.processors import SmartResize, ColorOverlay
from imagekit.lib import ImageColor
from cloudinary.models import CloudinaryField
import misaka
from groups.models import Group
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your models here.

class Post(models.Model):
    user = models.ForeignKey(User, related_name='posts', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=255)
    message = models.TextField()
    message_html = models.TextField(editable=False)
    image = CloudinaryField('image', blank=True, null=True)
    # image = models.ImageField(upload_to='post_images/', null=True)
    # thumbnail_image = ImageSpecField(source='image',
    #                                   processors=[SmartResize(300,300), ColorOverlay(color=ImageColor.getrgb('#454545'))],
    #                                   format='JPEG',
    #                                   options={'quality': 100})
    group = models.ForeignKey(Group, related_name='posts', blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.message

    def save(self, *args, **kwargs):
        self.message_html = misaka.html(self.message)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('posts:single', kwargs={'username':self.user.username,
                                               'pk':self.pk})

    class Meta():
        ordering = ['-created_at']
        unique_together = ['user', 'message']



class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='post_comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name='user_comments', on_delete=models.CASCADE)
    text = models.TextField()
    create_date = models.DateTimeField(default=timezone.now)

    parent_comment = models.ForeignKey('self', related_name='replies', on_delete=models.CASCADE, null=True)

    def get_absolute_url(self):
        return reverse('post_list')

    def __str__(self):
        return self.text

class Like(models.Model):
    post = models.ForeignKey(Post, related_name='post_likes', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='user_likes', on_delete=models.CASCADE)
