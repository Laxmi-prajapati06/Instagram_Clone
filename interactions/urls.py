from django.urls import path
from . import views
from django.contrib import messages

urlpatterns = [
    path('like/<int:post_id>/', views.toggle_like, name='toggle_like'),
    path('comment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('follow/<int:user_id>/', views.toggle_follow, name='toggle_follow'),
]