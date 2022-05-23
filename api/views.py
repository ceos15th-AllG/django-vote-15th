from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import *
from .models import *
from rest_framework import viewsets, views
# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class SignUpView(views.APIView):
    serializer_class = SignUpSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            token = RefreshToken.for_user(user)
            refresh = str(token)
            access = str(token.access_token)

            return JsonResponse({
                'user': user.username,
                'refresh': refresh,
                'access': access,
            })
        else:
            return JsonResponse(serializer.errors)