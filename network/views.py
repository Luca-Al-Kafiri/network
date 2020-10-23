from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
from django.core.paginator import Paginator, EmptyPage
from django.core.exceptions import ObjectDoesNotExist

from .models import User, Post, Follow

@csrf_exempt
def index(request):
    if request.method == "PUT":
        data = json.loads(request.body)
        post = Post.objects.get(id=data['id'])
        post.post = data["post"]
        post.save()
        return JsonResponse({"content": post.post})
    elif request.method == "POST":
        post = Post.objects.create()
        post.user = request.user.username
        post.post = request.POST.get('post')
        post.save()
        return redirect('index')
    else:
        p = Post.objects.all().order_by("-timestamp")
        post = Paginator(p, 10)
        if request.GET.get('page') == None:
            posts = post.page(1)
        else:
            try:
                posts = post.page(request.GET.get('page'))
            except:
                posts = post.page(1)
        return render(request, "network/index.html" , {'posts': posts})


@login_required
def follow(request):
    users= Follow.objects.filter(user=request.user.id)
    following = []
    for user in users:
        following.append(user.following)
    p = Post.objects.filter(user__in=following).order_by("-timestamp")
    post = Paginator(p, 10)
    if request.GET.get('page') == None:
        posts = post.page(1)
    else:
        try:
            posts = post.page(request.GET.get('page'))
        except:
            posts = post.page(1)
    return render(request, "network/following.html", {'posts': posts})


@login_required
def user(request, username):
    p = Post.objects.filter(user=username).order_by("-timestamp")
    post = Paginator(p, 10)
    if request.GET.get('page') == None:
        posts = post.page(1)
    else:
        try:
            posts = post.page(request.GET.get('page'))
        except:
            posts = post.page(1)
    id = User.objects.get(username=username)
    current_user = request.user.username
    following = Follow.objects.filter(user=id.id).count()
    followers = Follow.objects.filter(following=id.id).count()
    if request.method == "POST":
        try:
            f = Follow.objects.get(user=User.objects.get(username=current_user), following=User.objects.get(username= username))
            f.delete()
            status = 'Follow'
            following = Follow.objects.filter(user=id.id).count()
            followers = Follow.objects.filter(following=id.id).count()
        except ObjectDoesNotExist:
            f = Follow.objects.create(user=User.objects.get(username=current_user), following=User.objects.get(username= username))
            f.save()
            status = 'Unfollow'
            following = Follow.objects.filter(user=id.id).count()
            followers = Follow.objects.filter(following=id.id).count()
        return render(request, "network/user.html", {'posts': posts, 'followers': followers, "following": following, 'username': username, 'status': status})
    else:
        try:
            f = Follow.objects.get(user=User.objects.get(username=current_user), following=User.objects.get(username= username))
            status = 'Unfollow'
        except ObjectDoesNotExist:
            status = 'Follow'
        return render(request, "network/user.html", {'posts': posts, 'followers': followers, "following": following, 'username': username, 'status': status})


@csrf_exempt
@login_required
def like(request, id):
    if request.method == "PUT":
        data = json.loads(request.body)
        user=User.objects.get(username=request.user.username)
        post = Post.objects.get(id=id)
        if data['status'] == 'Like':
            user.like.add(post.id)
            user.save()
            post.liked = True
            post.save()
            if Post.objects.get(id=id).like.count() == 0:
                likes = 0
            else:
                likes = Post.objects.get(id=id).like.count()
            return JsonResponse({'status': 'Unlike', 'likes': likes})
        else:
           user.like.remove(post.id)
           user.save()
           post.liked = False
           post.save()
           if Post.objects.get(id=id).like.count() == 0:
               likes = 0
           else:
               likes = Post.objects.get(id=id).like.count()
           return JsonResponse({'status': 'Like', 'likes': likes})
    

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
