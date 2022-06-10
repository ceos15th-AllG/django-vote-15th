from django.db import models
from django.contrib.auth.models import AbstractUser


class Voter(AbstractUser):
    email = models.CharField(max_length=30, unique=True)
    voter_state = models.BooleanField(default=False)

    def __str__(self):
        return '[{}] {}'.format(self.id, self.username)


class Candidate(models.Model):
    candidate_name = models.CharField(max_length=20)
    part = models.CharField(max_length=20)
    description = models.TextField(null=True, blank=True)
    vote_cnt = models.IntegerField(default=0)

    def __str__(self):
        return '[{}] {}'.format(self.part, self.candidate_name)