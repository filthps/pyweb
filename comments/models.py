import uuid
from django.db import models
from django.contrib.auth import get_user_model


class Comment(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    text = models.CharField(max_length=300, blank=False)
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)
