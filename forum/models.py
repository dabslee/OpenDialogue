from django.conf import settings
from django.db import models

# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=500)
    content = models.TextField(max_length=20000)
    created = models.DateTimeField()
    
    views = models.IntegerField(default=0)
    agrees = models.IntegerField(default=0)
    agreechecks = models.IntegerField(default=0)
    strongs = models.IntegerField(default=0)
    strongchecks = models.IntegerField(default=0)