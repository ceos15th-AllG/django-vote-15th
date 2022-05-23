from django.urls import path, include
from rest_framework import urlpatterns, routers
from .views import *

app_name = 'api'

urlpatterns = [
    path('signup', SignUpView.as_view()),
]