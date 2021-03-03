from django.urls import path

from . import views

app_name = 'forum'
urlpatterns = [
    path('', views.index, name='index'),
    path('write_post', views.write_post, name='write_post'),
    path('post_successful', views.post_successful, name='post_successful'),
    path('post/<postid>', views.post, name='post'),
    path('explore', views.explore, name='explore'),
    path('account/<searchusername>', views.account, name='account'),
]
