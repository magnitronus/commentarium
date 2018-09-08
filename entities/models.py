from django.conf import settings
from django.db import models

class Post(models.Model):
    """Blog post"""
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
