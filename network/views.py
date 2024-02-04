import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from .models import User
from .forms import *


def index(request):
    posts = Post.objects.order_by("-created_at")
    return render(
        request,
        "network/index.html",
        {"posts": posts, "form": PostForm()},
    )


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
            return render(
                request,
                "network/login.html",
                {"message": "Invalid username and/or password."},
            )
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
            return render(
                request, "network/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request, "network/register.html", {"message": "Username already taken."}
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


@login_required
def post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.likes = 0
            post.save()
            return HttpResponseRedirect(reverse("index"))
    else:
        form = PostForm(request.POST)
    return render(
        request,
        "network/index.html",
        {
            "form": form,
        },
    )


@login_required
def allposts(request):
    posts = Post.objects.order_by("-created_at")
    paginator = Paginator(posts, 10)  
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(
        request,
        "network/posts.html",
        {"page_obj": page_obj,
         "paginator": paginator, 
         "form": CommentForm(),
         }
    )


@login_required
def profile(request):
    posts = Post.objects.all()
    current_users = User.objects.exclude(pk=request.user.id)
    user_following, __ = Follow.objects.get_or_create(pk=request.user.id)
    return render(
        request,
        "network/profile.html",
        {"all_users": current_users, "posts": posts, "following": user_following},
    )


@login_required
def follow(request, user_id):
    user_posts = Post.objects.filter(pk=user_id)
    following_model, __ = Follow.objects.get_or_create(pk=request.user.id)
    if user_id != request.user.id:
        user_to_follow = User.objects.get(pk=user_id)
        user_to_follow.followers.add(request.user.id)
        following_model.following.add(user_to_follow)
        return HttpResponseRedirect(reverse("following"))


@login_required
def unfollow(request, user_id):
    user_to_unfollow = User.objects.get(pk=user_id)
    follow_object = Follow.objects.get(pk=request.user.id)
    follow_object.following.remove(user_to_unfollow)
    return HttpResponseRedirect(reverse("profile"))


@login_required
def view_profile(request, user_id):
    following, created = Follow.objects.get_or_create(pk=user_id)
    posts = Post.objects.order_by("-created_at")
    followers_count = User.objects.get(pk=user_id).followers.count()
    if created:
        following.following.count = 0

    return render(
        request,
        "network/view.html",
        {
            "posts": posts,
            "username": User.objects.get(pk=user_id),
            "followers": followers_count,
            "following": following
        },
    )

@login_required
def comment(request, post_id):
    post = Post.objects.get(pk=post_id)
    comment, __ = Comment.objects.get_or_create(pk=post_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.comment_owner = request.user
            comment.save()

            post.comments.add(comment)
            return HttpResponseRedirect(reverse("allposts"))
    else:
        form = CommentForm(request.POST)
    return render(
        request,
        "network/posts.html",
        {
            "post": post,
            "comments": comment,
            "form": form,
        },
    )

def view_following(request):
    following = Follow.objects.filter(pk=request.user.id)
    return render(
        request,
        "network/following.html",
        {
            "following": following,
            "posts": Post.objects.all()
        },
    )

# def like(request, post_id):
#     posts = Post.objects.get(pk=post_id)
#     if request.user not in posts.reactions.all():
#         posts.reactions.add(request.user)
#         posts.likes += 1
#         posts.save()
#     return HttpResponseRedirect(reverse("allposts"))

@csrf_exempt       
def like(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)
        

    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    if request.method == "GET":
        return JsonResponse(post.serialize())

    elif request.method == "PUT":
        if request.user not in post.reactions.all():
            post.reactions.add(request.user)

            data = json.loads(request.body)
            if data.get("likes") is not None:
                post.likes = data["likes"]
            post.save()
            return HttpResponse(status=204)
        else:
            return JsonResponse({"message": "already liked."}, status=201)

    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)
