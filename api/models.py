from django.db import models
from django.contrib.auth.models import AbstractUser


class DateTime(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractUser):
    email = models.EmailField(max_length=100, unique=True)
    is_voted = models.BooleanField(default=False)


class Candidate(models.Model):
    name = models.CharField(max_length=10, unique=True)
    count = models.PositiveIntegerField(default=0)


class Vote(DateTime):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='votes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='votes')
