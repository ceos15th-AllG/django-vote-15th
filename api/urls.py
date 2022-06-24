from django.urls import path
from .views import *

urlpatterns = [
    path('signup', SignUpAPIView.as_view()),
    path('login', LoginAPIView.as_view()),
    path('vote', CandidateList.as_view()),
    path('vote/<part>', CandidateList.as_view()),
    path('vote/<part>/<int:pk>', CandidateDetail.as_view()),
    path('test', TestAPIView.as_view()),
]

