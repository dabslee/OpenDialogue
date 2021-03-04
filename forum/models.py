from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="author")
    title = models.CharField(max_length=500)
    content = models.TextField(max_length=20000)
    created = models.DateTimeField()
    parent = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="postparent", blank=True, null=True)
    parentid = models.IntegerField(blank=True, null=True)
    parenttitle = models.CharField(blank=True, max_length=500)
    parentauthor = models.CharField(blank=True, max_length=100)
    
    views = models.IntegerField(default=0)
    agrees = models.IntegerField(default=0)
    agreechecks = models.IntegerField(default=0)
    strongs = models.IntegerField(default=0)
    strongchecks = models.IntegerField(default=0)

class UserWrapper(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    viewed = models.ManyToManyField(Post, related_name='viewed', blank=True)
    agreed = models.ManyToManyField(Post, related_name='agreed', blank=True)
    disagreed = models.ManyToManyField(Post, related_name='disagreed', blank=True)
    stronged = models.ManyToManyField(Post, related_name='stronged', blank=True)
    weaked = models.ManyToManyField(Post, related_name='weaked', blank=True)
    reputation = models.IntegerField(default=0)