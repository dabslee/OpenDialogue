from django.contrib import admin
from .models import Post, UserWrapper

# Register your models here.
admin.site.register(Post)
admin.site.register(UserWrapper)