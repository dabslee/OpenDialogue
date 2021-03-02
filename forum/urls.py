from django.urls import path

from . import views

app_name = 'forum'
urlpatterns = [
    path('', views.index, name='index'),
    path('post', views.post, name='post'),
    path('post_successful', views.post_successful, name='post_successful')
]
