from django.shortcuts import render, redirect
from django.contrib.auth.models import Permission, User
from forum.models import Post
from forum.forms import PostForm

import datetime

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        context = {}
        context['user'] = request.user
        context['posts'] = Post.objects.all()
        return render(request, "index.html", context)
    else:
        return redirect('home')

def post(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        author = request.user
        new_post = Post(author=author, title=title, content=content, created=datetime.datetime.now())
        new_post.save()
        return redirect('forum:post_successful')
    else:
        context = {}
        context['user'] = request.user
        context["form"] = PostForm()
        return render(request, "post.html", context)

def post_successful(request):
    context = {}
    context['user'] = request.user
    return render(request, "post_successful.html", context)