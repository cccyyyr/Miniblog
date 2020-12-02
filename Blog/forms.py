
from .models import Post, Comment

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('post_text',)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment_text',)


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
