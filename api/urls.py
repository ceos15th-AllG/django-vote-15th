from django.urls import path
from api import views

urlpatterns = [
    path('signup/', views.Signup.as_view()),
    path('login/', views.LoginView.as_view()),
    path('vote/', views.Vote.as_view()),
]
