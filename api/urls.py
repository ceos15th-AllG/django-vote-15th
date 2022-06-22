from django.urls import path
from .views import *

urlpatterns = [
    path('test/', TestAPIView.as_view()),
    path('/signup', SignUpAPIView.as_view()),
    path('/login', LoginAPIView.as_view()),
]