from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, ProfileEditForm
from .models import CustomUser, Follow
from posts.models import Post

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('home_feed')
        
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully! Welcome to Instagram Clone!')
            return redirect('home_feed')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/signup.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home_feed')
        
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('home_feed')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('login')

@login_required
def profile_view(request, user_id):
    try:
        user = get_object_or_404(CustomUser, id=user_id)
        posts = Post.objects.filter(user=user).order_by('-created_at')
        
        followers_count = user.followers.count()
        following_count = user.following.count()
        

        is_following = Follow.objects.filter(
            follower=request.user,
            following=user
        ).exists()
        
        context = {
            'profile_user': user,
            'posts': posts,
            'followers_count': followers_count,
            'following_count': following_count,
            'is_following': is_following,
        }
        
        return render(request, 'users/profile.html', context)
    
    except Exception as e:
        print(f"Error loading profile: {str(e)}")
        import traceback
        traceback.print_exc()  
        messages.error(request, f'Error loading profile: {str(e)}')
        return redirect('home_feed')


@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile', user_id=request.user.id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProfileEditForm(instance=request.user)
    
    return render(request, 'users/edit_profile.html', {'form': form})