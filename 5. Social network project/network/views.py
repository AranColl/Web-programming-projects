import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post
from .forms import PostForm


def index(request):
    # Authenticated users view the index
    if request.user.is_authenticated:
        # add a new post to the feed
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                # create a new post
                new_post = Post()
                new_post.author = request.user.username
                new_post.text = form.cleaned_data["text_area"]
                new_post.like = 0
                new_post.save()

                # link it with the correct author (user)
                poster = User.objects.get(username=request.user.username)
                poster.posts.add(new_post)
                poster.save()
                return HttpResponseRedirect(reverse("index"))
        # show all the posts in the feed
        else:
            form = PostForm()
            all_posts = Post.objects.all().order_by('-timestamp')
            paginator = Paginator(all_posts, 5)
            page_number = request.GET.get('page')
            page = paginator.get_page(page_number)

            return render(request, "network/index.html",
                          {'form': form, 'page': page, "type": "Submit"})

    # Everyone else is prompted to sign in
    else:
        return HttpResponseRedirect(reverse("login"))


def profile(request, username):
    try:
        user_profile = User.objects.get(username=username)
        user_following = user_profile.following.count()
        user_followers = user_profile.followers.count()
        if user_profile.followers.filter(username=request.user).exists():
            bool_follow = "Unfollow"
        else:
            bool_follow = "Follow"
        post_list = Post.objects.filter(author=username).order_by('-timestamp')
        paginator = Paginator(post_list, 5)

        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)

        return render(request, "network/profile.html", {
            "username": username,
            "page": page,
            "user_followers": user_followers,
            "user_following": user_following,
            "bool_follow": bool_follow
        })
    except User.DoesNotExist:
        return render(request, "network/error.html", {"error": "This user does not yet exist"})


def following(request):
    all_posts = Post.objects.none()
    user_following = User.objects.get(username=request.user.username).following_list()
    for user in user_following:
        user_posts = User.objects.get(username=user).get_posts()
        all_posts |= user_posts

    paginator = Paginator(all_posts, 5)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, "network/index.html", {
        "page": page,
        "type": "hidden"
    })


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


@csrf_exempt
@login_required
def post(request, post_id):
    # get the requested post
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Requested post does not exist"}, status=404)

    # Return its content
    if request.method == "GET":
        return JsonResponse(post.serialize())

    # Update like condition
    elif request.method == "PUT":
        data = json.loads(request.body)
        if data.get("like") is not None:
            post.like = data["like"]
            post.save()
        elif data.get("new_text") is not None:
            post.text = data["new_text"]
            post.save()
        return HttpResponse(status=204)

    else:
        return JsonResponse({
            "error": "Wrong requested method"
        }, status=400)


@csrf_exempt
@login_required
def user(request, user_id):
    # get requested user
    try:
        user = User.objects.get(username=user_id)
    except User.DoesNotExist:
        return JsonResponse({"error": "Requested user does not exist"}, status=404)

    # Return its content
    if request.method == "GET":
        return JsonResponse(user.serialize())

    # Update follow condition
    elif request.method == "PUT":
        data = json.loads(request.body)
        if data.get("new_follower") is not None:
            user_follow = User.objects.get(username=data["new_follower"])
            user.following.add(user_follow)
            user.save()
            user_follow.followers.add(user)
            user_follow.save()
        elif data.get("new_unfollower") is not None:
            user_unfollow = User.objects.get(username=data["new_unfollower"])
            user.following.remove(user_unfollow)
            user.save()
            user_unfollow.followers.remove(user)
            user_unfollow.save()

        return HttpResponse(status=204)

    else:
        return JsonResponse({
            "error": "Wrong requested method"
        }, status=400)
