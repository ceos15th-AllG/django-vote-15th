from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(max_length=100, unique=True)
    is_voted = models.BooleanField(default=False)


class Candidate(models.Model):
    name = models.CharField(max_length=10)
    count = models.PositiveIntegerField(default=0)


class Vote(models.Model):
    candidate_id = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
