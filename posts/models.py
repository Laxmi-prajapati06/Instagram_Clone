from django.db import models
from users.models import CustomUser

class Post(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='posts')
    image = models.ImageField(upload_to='post_images/', null=True, blank=True)  
    caption = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s post"