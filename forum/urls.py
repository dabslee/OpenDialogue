from django.urls import path

from . import views

app_name = 'forum'
urlpatterns = [
    path('', views.index, name='index'),
    path('write_post', views.write_post, name='write_post'),
    path('post_successful', views.post_successful, name='post_successful'),
    path('post/<postid>', views.post, name='post'),
    path('agree/<postid>', views.agree, name='agree'),
    path('disagree/<postid>', views.disagree, name='disagree'),
    path('strong/<postid>', views.strong, name='strong'),
    path('weak/<postid>', views.weak, name='weak'),
    path('explore', views.explore, name='explore'),
    path('account/<searchusername>', views.account, name='account'),
]
