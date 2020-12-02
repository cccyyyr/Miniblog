from .models import Post, HashTag, Liked
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login
from django. contrib import messages
import re
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.utils import timezone
from django.http import HttpResponseRedirect

from .forms import PostForm, UserRegisterForm, CommentForm


def splash(request):
    return render(request, 'registration/splash.html')

def create(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.pub_date = timezone.now()
            sentences = post.post_text.split(" ")
            post.save()
            for sentence in sentences:
                tags = sentence.split("#")[1:]
                for t in tags:
                    ht = HashTag.objects.filter(tag_text=t)
                    if ht.count() > 0:
                        post.tags.add(ht[0])
                    else:
                        ht = HashTag()
                        ht.tag_text = t
                        ht.save()
                        post.tags.add(ht)
                        ht.save()
            post.save()
            return redirect(home)
    else:
         form = PostForm()
    return render(request, 'blog/create.html', {'form': form})


def home(request):
    post_list = Post.objects.all()
    tag_list = HashTag.objects.all()
    context = {'post_list': post_list,
               'tag_list': tag_list}
    return render(request, 'registration/home.html', context)


def viewmy(request):
    post_list = request.user.post_set.all()
    context = {'post_list': post_list}
    return render(request, 'blog/viewmypost.html', context)

def viewothers(request, author_id=None):
    post_list = Post.objects.filter(author__id=author_id)
    context = {
        'author': User.objects.get(id=author_id),
        'post_list': post_list}
    return render(request, 'blog/viewotherspost.html', context)

class SignUp(generic.CreateView):
    form_class = UserRegisterForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

def delete_post(request, post_id=None):
    post_to_delete = Post.objects.get(id=post_id)
    if request.user == post_to_delete.author:
        post_to_delete.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def like_post(request, post_id=None):
    post_to_like = Post.objects.get(id=post_id)
    user = request.user
    if Liked.objects.filter(post=post_to_like, user=user).count() > 0:
        post_to_like.likes -= 1
        relation = Liked.objects.filter(post=post_to_like, user=user)[0]
        relation.delete()
    else:
        post_to_like.likes += 1
        relation = Liked()
        relation.post = post_to_like
        relation.user = user
        relation.save()
    post_to_like.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

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

def tag(request, tag_id=None):
    tag = HashTag.objects.get(id=tag_id)
    posts = tag.post_set.all()
    tag_name = tag.tag_text
    return render(request, 'blog/viewtag.html', {'post_list': posts,
                                                 'tag_text': tag_name})