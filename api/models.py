from django.db import models
from django.contrib.auth.models import *


class User(AbstractUser):
    voteChecker = models.BooleanField(default=False)
    created_on = models.DateTimeField("등록일자", auto_now_add=True)
    updated_on = models.DateTimeField("수정일자", auto_now=True)


class Candidate(models.Model):
    count = models.IntegerField(default=0)
    name = models.CharField(max_length=150)
    image = models.TextField()
    content = models.TextField()


class Vote(models.Model):
    voter_name = models.OneToOneField(User, on_delete=models.CASCADE, related_name='vote_user')
    candidate_name = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='voted_candidate')

