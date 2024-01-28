from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import User
from .forms import *


def index(request):
    posts = Post.objects.order_by("-created_at")

    return render(
        request,
        "network/index.html",
        {"posts": posts, "form": ListingPost()},
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
        form = ListingPost(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return HttpResponseRedirect(reverse("index"))
    else:
        form = ListingPost(request.POST)
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
    paginator = Paginator(posts, 1)  
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(
        request,
        "network/posts.html",
        {"page_obj": page_obj,
         "paginator": paginator}
    )


@login_required
def profile(request):
    posts = Post.objects.all()
    current_users = User.objects.all()
    user_following, __ = Follow.objects.get_or_create(pk=request.user.id)
    print(user_following.following.count())
    return render(
        request,
        "network/profile.html",
        {"all_users": current_users, "posts": posts, "followers": user_following},
    )


@login_required
def follow(request, user_id):
    user_posts = Post.objects.filter(pk=user_id)
    following_model, __ = Follow.objects.get_or_create(pk=request.user.id)
    if user_id != request.user.id:
        user_to_follow = User.objects.get(pk=user_id)
        user_to_follow.followers.add(request.user.id)
        following_model.following.add(user_to_follow)
        return render(
            request,
            "network/following.html",
            {
                "posts": user_posts,
                "followers": user_to_follow.followers.count(),
                "following": Follow.objects.get(pk=user_id),
            },
        )

@login_required
def unfollow(request, user_id):
    user_to_unfollow = User.objects.get(pk=user_id)
    follow_object = Follow.objects.get(pk=request.user.id)
    follow_object.following.remove(user_to_unfollow)
    return HttpResponseRedirect(reverse("profile"))


@login_required
def view_profile(request, user_id):
    return render(
        request,
        "network/view.html",
        {
            "posts": Post.objects.filter(pk=user_id),
            "username": User.objects.get(pk=user_id),
            "followers": User.objects.get(pk=user_id).followers.count(),
            "following": Follow.objects.get(pk=user_id),
        },
    )

