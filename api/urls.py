from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter


urlpatterns = [
    path("auth/signUp", SignUpApi.as_view()),
    path("auth/login", LoginApi.as_view()),
    path("auth/users", UserApi.as_view()),

]


