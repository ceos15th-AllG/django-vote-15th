from rest_framework import routers
from django.urls import path, include
from .views import *

router = routers.DefaultRouter()
router.register(r'candidates', CandidateViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('users/signups/', SignUpView.as_view()),
    path('users/logins/', SignInView.as_view()),
    path('votes/<int:pk>/', VoteView.as_view()),
]
