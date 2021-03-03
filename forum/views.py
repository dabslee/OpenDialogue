from django.shortcuts import render, redirect
from django.contrib.auth.models import Permission, User
from forum.models import Post, UserWrapper
from forum.forms import PostForm
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist

import datetime

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return redirect('home')
    if request.user.is_authenticated:
        context = {}
        context['user'] = request.user
        context['posts'] = Post.objects.all()
        return render(request, "index.html", context)
    else:
        return redirect('home')

def write_post(request):
    if not request.user.is_authenticated:
        return redirect('home')
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
        return render(request, "write_post.html", context)

def post_successful(request):
    if not request.user.is_authenticated:
        return redirect('home')
    context = {}
    context['user'] = request.user
    return render(request, "post_successful.html", context)

def post(request, postid):
    if not request.user.is_authenticated:
        return redirect('home')
    context = {}
    context['user'] = request.user
    thepost = Post.objects.get(id=postid)
    context['post'] = thepost
    try:
        UserWrapper.objects.get(user=request.user)
    except ObjectDoesNotExist:
        UserWrapper.objects.create(user=request.user)
    if not UserWrapper.objects.filter(user=request.user).filter(viewed=thepost).exists():
        thepost.views += 1
        thepost.save()
        UserWrapper.objects.get(user=request.user).viewed.add(thepost)
    return render(request, "post.html", context)

def explore(request):
    if not request.user.is_authenticated:
        return redirect('home')
        
    context = {}
    context['user'] = request.user
    if request.method == "POST":
        query = request.POST.get("query")
        sortby = request.POST.get("sortby")
        context['posts'] = Post.objects.filter(\
            Q(author__username__icontains=query) |\
                Q(title__icontains=query) |\
                    Q(content__icontains=query))
        if sortby == "date":
            context['posts'] = context['posts'].order_by('-created')
        elif sortby == "alpha":
            context['posts'] = context['posts'].order_by('title')
        elif sortby == "views":
            context['posts'] = context['posts'].order_by('-views')
        return render(request, "explore.html", context)
    else:
        context['posts'] = []
        return render(request, "explore.html", context)

def account(request, searchusername):
    if not request.user.is_authenticated:
        return redirect('home')
    context = {}
    context['user'] = request.user
    context['searcheduser'] = User.objects.get(username=searchusername)
    context['posts'] = Post.objects.filter(Q(author__username=searchusername))
    context['totalviews'] = sum(post.views for post in context['posts'])
    return render(request, "account.html", context)