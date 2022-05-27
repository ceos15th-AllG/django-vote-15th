from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, default='valid')

    class Meta:
        abstract = True


class UserManager(BaseUserManager):
    def create_user(self, name, email, password):
        if not name:
            raise ValueError('이름을 꼭 써주세요')
        elif not email:
            raise ValueError('이메일을 꼭 써주세요')
        user = self.model(
            name=name,
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, email, password):
        user = self.create_user(
            name=name,
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    name = models.CharField(max_length=6)
    email = models.CharField(max_length=30, unique=True)
    password = models.TextField()
    part = models.CharField(max_length=3)
    team = models.CharField(max_length=14, default='')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'password', 'part', 'team']

    def __str__(self):
        return self.name


class Candidate(BaseModel):
    user_name = models.CharField(max_length=6)
    age = models.PositiveIntegerField()
    part = models.CharField(max_length=10)
    vote_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return '{} : {}'.format(self.user_name, self.part)


class Vote(BaseModel):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='candidate_votes')
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='user_votes')

    def __str__(self):
        return '{} : {}'.format(self.candidate.user_name, self.user.user_name)
