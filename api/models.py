from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(max_length=64, unique=True)


class Candidate(models.Model):
    part = models.CharField(max_length=1)
    name = models.CharField(max_length=30)
    vote_num = models.BigIntegerField(default=0)

    def __str__(self):
        return self.name
