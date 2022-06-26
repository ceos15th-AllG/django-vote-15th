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
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='votes')
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='votes')
    #related_nameds
    # https://fabl1106.github.io/django/2019/05/27/Django-26.-%EC%9E%A5%EA%B3%A0-related_name-%EC%84%A4%EC%A0%95%EB%B0%A9%EB%B2%95.html

