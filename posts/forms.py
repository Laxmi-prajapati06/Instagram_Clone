from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['image', 'caption']
        widgets = {
            'caption': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Write a caption...',
                'class': 'form-control'
            }),
        }