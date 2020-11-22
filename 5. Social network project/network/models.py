from django.contrib.auth.models import AbstractUser
from django.db import models


class Post(models.Model):
    author = models.CharField(max_length=60)
    text = models.CharField(max_length=280)
    timestamp = models.DateTimeField(auto_now_add=True)
    like = models.IntegerField()

    def serialize(self):
        return {
            "id": self.id,
            "author": self.author,
            "text": self.text,
            "timestamp": self.timestamp.strftime("%b %-d %Y, %-I:%M %p"),
            "like": self.like
        }


class User(AbstractUser):
    followers = models.ManyToManyField("User", related_name="user_followers")
    following = models.ManyToManyField("User", related_name="user_following")
    posts = models.ManyToManyField("Post", related_name="user_posts")

    def serialize(self):
        return {
            "following": [user.username for user in self.following.all()],
            "posts": [posts.id for posts in self.posts.all()],
            "num_followers": self.followers.count(),
            "num_following": self.following.count()
        }

    def following_list(self):
        return [user.username for user in self.following.all()]

    def get_posts(self):
        return self.posts.all()
