from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
#router.register(r'users', UserViewSet)
router.register(r'candidates', CandidateViewSet)
#router.register(r'votes', VoteViewSet)
urlpatterns = router.urls
