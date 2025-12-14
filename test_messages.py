import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Instagram_Clone.settings')
django.setup()

try:
    from django.contrib import messages
    from interactions.views import toggle_like, add_comment, toggle_follow
    from posts.views import create_post, home_feed
    from users.views import signup_view, login_view, logout_view, profile_view
    
    print("All imports successful!")
    
    print(f"✓ Messages module: {messages}")

    views_with_messages = [
        ('toggle_like', toggle_like),
        ('add_comment', add_comment),
        ('toggle_follow', toggle_follow),
        ('create_post', create_post),
        ('signup_view', signup_view),
        ('login_view', login_view),
        ('logout_view', logout_view),
    ]
    
    print("\nViews using messages:")
    for name, view in views_with_messages:
        print(f"  ✓ {name}")
    
except ImportError as e:
    print(f"✗ Import error: {e}")
except Exception as e:
    print(f"✗ Error: {e}")