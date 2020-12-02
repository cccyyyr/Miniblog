from django.db import models
from django.contrib.auth.models import User


class HashTag(models.Model):
    tag_text = models.TextField()

    def __str__(self):
        return self.tag_text


class Post(models.Model):
    post_text = models.TextField()
    pub_date = models.DateTimeField('date published')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(HashTag)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return self.post_text


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    pub_date = models.DateTimeField('date published')
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.comment_text

class Liked(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
