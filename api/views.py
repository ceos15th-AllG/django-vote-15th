from django.core import exceptions
from django.http import JsonResponse
from django.shortcuts import render

from rest_framework import status
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .serializers import *
from .models import *

class Signup(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # jwt token
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "username": user.username,
                    "email": user.email,
                    "voted_fe": user.voted_fe,
                    "voted_be": user.voted_be,
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


class LoginView(APIView):
    def post(self, request):
        username = request.data['username']
        password = request.data['password']

        user = User.objects.filter(username=username).first()

        if user is not None:
            if password == user.password:
                token = TokenObtainPairSerializer.get_token(user)
                refresh_token = str(token)
                access_token = str(token.access_token)
                res = Response(
                    {
                        "username": user.username,
                        "message": "Login success!",
                        "token": {
                            "access": access_token,
                            "refresh": refresh_token,
                        },
                    },
                    status=status.HTTP_200_OK
                )
                res.set_cookie("username", user.username, httponly=True)
                res.set_cookie("access", access_token, httponly=True)
                res.set_cookie("refresh", refresh_token, httponly=True)
                return res

            else:
                return Response({'message': 'Wrong password!'}, status=status.HTTP_401_UNAUTHORIZED)

        elif user is None:
                return Response({'message': 'User not found!'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'message': 'Login failed!'}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    def post(self, request):
        res = JsonResponse({
            "message": "Logged out"
        })
        res.delete_cookie('username')
        res.delete_cookie('access')
        res.delete_cookie('refresh')
        return res


class Vote(APIView):
    def get(self, request):  # vote 현황 가져오기
        candidates = Candidate.objects.all().order_by('-vote_cnt')
        serializer = CandidateSerializer(candidates, many=True)
        return Response(serializer.data)

    def post(self, request):
        candidate_name = self.request.data['candidate']
        candidate = Candidate.objects.get(candidate_name=candidate_name)

        user_name = request.COOKIES.get('username')
        try:
            user = User.objects.get(username=user_name)
        except User.DoesNotExist:
            return Response({'message': '투표는 로그인이 필요합니다!'}, status=status.HTTP_400_BAD_REQUEST)

        # token = request.COOKIES.get('access')

        if not user.voted_be:  # 아직 투표하지 않은 투표자라면
            candidate.vote_cnt = candidate.vote_cnt + 1
            candidate.save()
            user.voted_be = True
            user.save()
            return JsonResponse({
                'message': 'success!',
                'user_name': user_name,
                'candidate_name': candidate_name,
                'vote_cnt': candidate.vote_cnt}, status=HTTP_201_CREATED)
        else:  # 이미 투표를 했다면 투표권 X
            return JsonResponse({'message': '투표는 1회만 가능합니다.'}, status=status.HTTP_401_UNAUTHORIZED)