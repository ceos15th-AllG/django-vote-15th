from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, default='valid')

    class Meta:
        abstract = True


class User(BaseModel):
    user_name = models.CharField(max_length=4)
    password = models.CharField(max_length=20)
    email = models.CharField(max_length=30)
    part = models.CharField(max_length=10)

    def __str__(self):
        return '{} : {}'.format(self.user_name, self.part)


class Candidate(BaseModel):
    user_name = models.CharField(max_length=4)
    age = models.PositiveIntegerField()
    part = models.CharField(max_length=10)
    vote_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return '{} : {}'.format(self.user_name, self.part)


class Vote(BaseModel):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='candidate_votes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_votes')

    def __str__(self):
        return '{} : {}'.format(self.candidate.user_name, self.user.user_name)
