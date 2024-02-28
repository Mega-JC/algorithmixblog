from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime

class User(AbstractUser):
    bio = models.CharField(max_length=1024, blank=True)
    followers = models.ManyToManyField("self", blank=True, symmetrical=False, related_name="following")

    def serialize_preview(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "created": {
                "ftimestamp": self.date_joined.strftime("%d %b %Y, %I:%M:%S %p").title(),
                "timestamp": int(self.date_joined.astimezone(tz=datetime.timezone.utc).timestamp()*1000_000_000)
            },
            "follower_count": self.followers.count(),
            "following_count": self.following.count(),
            "bio": self.bio,
    }


class BlogPostTag(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"BlogPostTag({self.name})"


class BlogPost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blogposts")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=256, blank=True)
    text = models.CharField(max_length=40960)
    likers = models.ManyToManyField(User, blank=True, related_name="liked_blogposts")
    favorers = models.ManyToManyField(User, blank=True, related_name="favorite_blogposts")
    tags = models.ManyToManyField(BlogPostTag, blank=True, related_name="related_blogposts")
    cover_url = models.URLField(blank=True, max_length=1024)
    is_private = models.BooleanField(default=True)

    def serialize_preview(self):
        return {
            "id": self.id,
            "is_private": self.is_private,
            "author": {
                "username": self.author.username,
                "id": self.author.id,    
            },
            "title": self.title,
            "description": self.description,
            "like_count": self.likers.count(),
            "comment_count": self.comments.count(),
            "tags": [ tag.name for tag in self.tags.all() ],
            "cover_url": self.cover_url if self.cover_url else None,
            "created": {
                "ftimestamp": self.created.strftime("%d %b %Y").title(),
                "timestamp": int(self.created.astimezone(tz=datetime.timezone.utc).timestamp()*1000_000_000)
            },
            "updated": {
                "ftimestamp": self.updated.strftime("%d %b %Y").title(),
                "timestamp": int(self.updated.astimezone(tz=datetime.timezone.utc).timestamp()*1000_000_000)
            }
        }

    def __str__(self):
        return f"BlogPost {self.id} by {self.author} on {self.created}"


class BlogPostComment(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blogpost_comments")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=4096)
    likers = models.ManyToManyField(User, blank=True, related_name="liked_blogpost_comments")
    reference = models.ForeignKey("self", blank=True, on_delete=models.SET_NULL, null=True, related_name="replies")
    had_reference = models.BooleanField(default=False)
    is_censored = models.BooleanField(default=False)

    def serialize(self, references=True):
        output = {
            "post_id": self.post.id,
            "id": self.id,
            "author": self.author.username,
            "text": self.text,
            "like_count": self.likers.count(),
            "created": {
                "ftimestamp": self.created.strftime("%d %b %Y").title(),
                "timestamp": int(self.created.astimezone(tz=datetime.timezone.utc).timestamp()*1000_000_000)
            },
            "updated": {
                "ftimestamp": self.updated.strftime("%d %b %Y").title(),
                "timestamp": int(self.updated.astimezone(tz=datetime.timezone.utc).timestamp()*1000_000_000)
            }
        }

        if references and self.reference not in (None, False, "NULL"):
            output.update({"reference": self.reference.serialize(references=False)})

        return output

    def __str__(self):
        return f"Comment on '{self.post}' by {self.author} on {self.created}" +\
            (f"(edited {self.updated})" if self.created != self.updated else "")
