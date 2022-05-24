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
                'message': 'Signup succeeded',
                'user': user.username,
                'access': access,
                'refresh': refresh,
            })
        else:
            return JsonResponse(serializer.errors)


class LoginView(views.APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = serializer.validated_data['refresh']
            access = serializer.validated_data['access']

            return JsonResponse({
                'message': 'Login succeeded',
                'user': user.username,
                'is_voted': user.is_voted,
                'access': access,
                'refresh': refresh,
            })

        else:
            return JsonResponse(serializer.errors)