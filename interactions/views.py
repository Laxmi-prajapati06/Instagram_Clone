from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages 
from django.http import JsonResponse
from posts.models import Post
from users.models import CustomUser, Follow
from .models import Like, Comment

@login_required
def toggle_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    

    like_exists = Like.objects.filter(user=request.user, post=post).exists()
    
    if like_exists:
        Like.objects.filter(user=request.user, post=post).delete()
        liked = False
        message = "Post unliked"
    else:
        Like.objects.create(user=request.user, post=post)
        liked = True
        message = "Post liked"
    
    messages.success(request, message)
    return redirect('home_feed')

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if request.method == 'POST':
        text = request.POST.get('text', '').strip()
        if text:
            Comment.objects.create(user=request.user, post=post, text=text)
        else:
            messages.error(request, 'Write a comment!')
    
    return redirect('home_feed')

@login_required
def toggle_follow(request, user_id):
    user_to_follow = get_object_or_404(CustomUser, id=user_id)
    

    if request.user == user_to_follow:
        messages.error(request, "You cannot follow yourself!")
        return redirect('profile', user_id=user_id)
    

    follow_exists = Follow.objects.filter(
        follower=request.user,
        following=user_to_follow
    ).exists()
    
    if follow_exists:
        Follow.objects.filter(
            follower=request.user,
            following=user_to_follow
        ).delete()
        messages.success(request, f"You have unfollowed {user_to_follow.username}")
        followed = False
    else:
        Follow.objects.create(
            follower=request.user,
            following=user_to_follow
        )
        messages.success(request, f"You are now following {user_to_follow.username}")
        followed = True
    
    return redirect('profile', user_id=user_id)