from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from api.serializers import *


class Signup(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            voter = serializer.save()
            # jwt token
            token = TokenObtainPairSerializer.get_token(voter)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "username": voter.username,
                    "password": voter.password,
                    "email": voter.email,
                    "message": "success!",
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                },
                status=status.HTTP_200_OK,
            )
            return res
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
