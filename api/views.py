from .serializers import *
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class SignUpAPIView(APIView):

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            token = RefreshToken.for_user(user)

            return Response({
                "user": user.username,
                "message": "Sign up Success",
                "refresh": str(token),
                "access": str(token.access_token),
            })

        else:
            return Response(serializer.errors)


class LoginAPIView(APIView):
    def post(self, request):
        username = request.data.get('username', None)
        password = request.data.get('password', None)
        user = authenticate(username=username, password=password)

        if user is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            token = RefreshToken.for_user(user)

            return Response(
                {
                    "user": user.username,
                    "message": "Login Success",
                    "refresh": str(token),
                    "access": str(token.access_token),

                }
            )


class TestAPIView(APIView):
    def get(self):
        return Response({"msg": "hello"})
