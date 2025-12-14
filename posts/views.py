from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Post
from .forms import PostForm
from users.models import Follow, CustomUser
from interactions.models import Like, Comment

@login_required
def post_creation(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            messages.success(request, 'Post created successfully!')
            return redirect('home_feed')
        else:
            messages.error(request, 'Please check the form for errors.')
    else:
        form = PostForm()
    
    context = {'form': form}
    return render(request, 'posts/create_post.html', context)

@login_required
def home_feed(request):
    following_ids = Follow.objects.filter(follower=request.user).values_list('following_id', flat=True)
        

    following_ids = list(following_ids) + [request.user.id]
        
    feed_posts = Post.objects.filter(user_id__in=following_ids).order_by('-created_at')

    for post in feed_posts:
        post.likes_count = post.likes.count()
        post.comments_list = post.comments.all().order_by('-created_at')[:5]
        post.user_has_liked = post.likes.filter(user=request.user).exists()
        
    suggested_users = CustomUser.objects.exclude(
        id__in=list(following_ids)
    ).exclude(
        id=request.user.id
    )[:5]
        
    return render(request, 'posts/feed.html', {
        'posts': feed_posts,
        'suggested_users': suggested_users
    })
    