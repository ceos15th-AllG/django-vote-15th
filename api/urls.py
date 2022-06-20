from rest_framework import routers
from django.urls import path, include
from .views import *

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('users/signups/', SignUpView.as_view()),
    path('users/logins/', SignInView.as_view()),
    path('votes/', VoteView.as_view()),
    path('candidates/', CandidateView.as_view()),
]
