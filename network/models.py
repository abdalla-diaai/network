from django.contrib.auth.models import AbstractUser
from django import forms
from django.db import models
from django.conf import settings


class User(AbstractUser):
    pass

class Follow(models.Model):
    following = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="followers", symmetrical=False)
    def __str__(self) -> str:
        return f"{self.following}"


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-updating
    ``created_at`` and ``updated_at`` fields.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True




class Post(TimeStampedModel):
    created = TimeStampedModel.created_at
    body = models.CharField(max_length=300)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    likes = models.IntegerField(blank=True)
    reactions = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="user_reactions", symmetrical=False)
    def __str__(self) -> str:
        return f"{self.user} {self.body}"


class Comment(TimeStampedModel):
    comment_owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    comment_created = TimeStampedModel.created_at
    comment_body = models.CharField(max_length=300)
    post_comments = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments",
        blank=True,
        null=True,
    )

    def __str__(self) -> str:
        return f"{self.comment_owner} {self.comment_body}"

