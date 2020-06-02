from .models import Post
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login
from django. contrib import messages

from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.utils import timezone
from django.http import HttpResponseRedirect

from .forms import PostForm, UserRegisterForm, CommentForm



def create(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.pub_date = timezone.now()
            post.save()
            return redirect(home)
    else:
        form = PostForm()
    return render(request, 'blog/create.html', {'form': form})


def home(request):
    post_list = Post.objects.all()
    context = {'post_list': post_list}
    return render(request, 'registration/home.html', context)


def viewmy(request):
    post_list = request.user.post_set.all()
    context = {'post_list': post_list}
    return render(request, 'blog/viewmypost.html', context)


class SignUp(generic.CreateView):
    form_class = UserRegisterForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


def delete_post(request, post_id=None):
    post_to_delete = Post.objects.get(id=post_id)
    post_to_delete.delete()
    return HttpResponseRedirect('/viewmypost/')

def like_post(request, post_id=None):
    post_to_like = Post.objects.get(id=post_id)
    post_to_like.likes += 1
    post_to_like.save()
    return HttpResponseRedirect('/')

def comment(request, post_id=None):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            post = Post.objects.get(id = post_id)
            c = form.save(commit=False)
            c.pub_date = timezone.now()
            c.author = request.user
            c.post = post
            c.save()
            return redirect('home')
    else:
            form = CommentForm()
    return render(request, 'blog/comment.html', {'form': form})

