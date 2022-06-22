from django.urls import path
from .views import *

urlpatterns = [
    path('signup', SignUpAPIView.as_view()),
    path('login', LoginAPIView.as_view()),
    path('test', TestAPIView.as_view()),
]