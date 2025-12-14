from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    
    def __str__(self):
        return self.username

class Follow(models.Model):
    follower = models.ForeignKey(CustomUser, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(CustomUser, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('follower', 'following')
    
    def __str__(self):
        return f"{self.follower} follows {self.following}"