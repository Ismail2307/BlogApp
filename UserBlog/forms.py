from django import forms
from .models import *

class CreateBlog(forms.ModelForm):
    class Meta:
        model= Blog
        fields = ['title', 'description']

class CreatePost(forms.ModelForm):
    class Meta:
        model= Post
        fields = ['title', 'content']




