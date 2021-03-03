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
    UserWrapper.objects.get_or_create(user=request.user)
    if not UserWrapper.objects.filter(user=request.user).filter(viewed=thepost).exists():
        thepost.views += 1
        thepost.save()
        UserWrapper.objects.get(user=request.user).viewed.add(thepost)
    if UserWrapper.objects.filter(user=request.user).filter(agreed=thepost).exists():
        context['agreed'] = True
    else:
        context['agreed'] = False
    if UserWrapper.objects.filter(user=request.user).filter(disagreed=thepost).exists():
        context['disagreed'] = True
    else:
        context['disagreed'] = False
    if UserWrapper.objects.filter(user=request.user).filter(stronged=thepost).exists():
        context['stronged'] = True
    else:
        context['stronged'] = False
    if UserWrapper.objects.filter(user=request.user).filter(weaked=thepost).exists():
        context['weaked'] = True
    else:
        context['weaked'] = False
        
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

def agree(request, postid):
    if not request.user.is_authenticated:
        return redirect('home')
    context = {}
    context['user'] = request.user
    thepost = Post.objects.get(id=postid)
    UserWrapper.objects.get_or_create(user=request.user)
    if not UserWrapper.objects.filter(user=request.user).filter(agreed=thepost).exists():
        thepost.agrees += 1
        if not UserWrapper.objects.filter(user=request.user).filter(disagreed=thepost).exists():
            thepost.agreechecks += 1
        else:
            UserWrapper.objects.get(user=request.user).disagreed.remove(thepost)
        thepost.save()
        UserWrapper.objects.get(user=request.user).agreed.add(thepost)
    return redirect('forum:post', postid=postid)

def disagree(request, postid):
    if not request.user.is_authenticated:
        return redirect('home')
    context = {}
    context['user'] = request.user
    thepost = Post.objects.get(id=postid)
    UserWrapper.objects.get_or_create(user=request.user)
    if not UserWrapper.objects.filter(user=request.user).filter(disagreed=thepost).exists():
        if not UserWrapper.objects.filter(user=request.user).filter(agreed=thepost).exists():
            thepost.agreechecks += 1
        else:
            thepost.agrees -= 1
            UserWrapper.objects.get(user=request.user).agreed.remove(thepost)
        thepost.save()
        UserWrapper.objects.get(user=request.user).disagreed.add(thepost)
    return redirect('forum:post', postid=postid)

def strong(request, postid):
    if not request.user.is_authenticated:
        return redirect('home')
    context = {}
    context['user'] = request.user
    thepost = Post.objects.get(id=postid)
    UserWrapper.objects.get_or_create(user=request.user)
    if not UserWrapper.objects.filter(user=request.user).filter(stronged=thepost).exists():
        thepost.strongs += 1
        if not UserWrapper.objects.filter(user=request.user).filter(weaked=thepost).exists():
            thepost.strongchecks += 1
        else:
            UserWrapper.objects.get(user=request.user).weaked.remove(thepost)
        thepost.save()
        UserWrapper.objects.get(user=request.user).stronged.add(thepost)
    return redirect('forum:post', postid=postid)

def weak(request, postid):
    if not request.user.is_authenticated:
        return redirect('home')
    context = {}
    context['user'] = request.user
    thepost = Post.objects.get(id=postid)
    UserWrapper.objects.get_or_create(user=request.user)
    if not UserWrapper.objects.filter(user=request.user).filter(weaked=thepost).exists():
        if not UserWrapper.objects.filter(user=request.user).filter(stronged=thepost).exists():
            thepost.strongchecks += 1
        else:
            thepost.strongs -= 1
            UserWrapper.objects.get(user=request.user).stronged.remove(thepost)
        thepost.save()
        UserWrapper.objects.get(user=request.user).weaked.add(thepost)
    return redirect('forum:post', postid=postid)