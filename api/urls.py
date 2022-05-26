from rest_framework import routers
from django.urls import path, include
from .views import *

router = routers.DefaultRouter()
router.register(r'candidates', CandidateViewSet)
router.register(r'votes', VoteViewSet)
# urlpatterns = router.urls

urlpatterns = [
    path('', include(router.urls)),
    path('signups/', SignUpView.as_view())
]
