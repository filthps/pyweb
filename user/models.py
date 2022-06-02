from django.db import models
from django.contrib.auth.models import AbstractUser
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


class ExtendedUser(AbstractUser):
    avatar = models.ImageField(upload_to="", blank=True, null=True, default=None)
    avatar_thumb = ImageSpecField(source='avatar',
                                  processors=[ResizeToFill(75, 75)], format='PNG', options={'quality': 75})
