from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView
)

urlpatterns = [
    path('signup/', SignupView.as_view()),

    path('login/', LoginView.as_view()),
    path('login/user/', UserView.as_view()),
    path('logout/', LogoutView.as_view()),

    path('candidate/', CandidateView.as_view()),

    path('vote/', VoteView.as_view()),

    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
