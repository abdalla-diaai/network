from django.contrib.auth.models import AbstractUser
from django import forms
from django.db import models
from django.conf import settings


class User(AbstractUser):
    pass

class Follow(models.Model):
    following = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="followers")

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

    def __str__(self) -> str:
        return f"{self.user} {self.body}"

