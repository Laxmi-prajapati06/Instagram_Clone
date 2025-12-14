from django.contrib.auth import get_user_model
from .models import Follow

User = get_user_model()

def instagram_context(request):
    context = {}
    
    if request.user.is_authenticated:
        following = Follow.objects.filter(follower=request.user).values_list('following_id', flat=True)
        context['following_users'] = User.objects.filter(id__in=following)
        
        all_users = User.objects.exclude(id=request.user.id)
        context['all_users'] = all_users
        
    return context