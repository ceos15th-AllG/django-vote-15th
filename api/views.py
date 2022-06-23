import jwt
from django.contrib.auth import authenticate
from django.core import exceptions
from django.http import JsonResponse
from django.shortcuts import render

from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .serializers import *
from .models import *

import os
import environ
import tokenize

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
env = environ.Env(
    DEBUG=(bool, False)
)

environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

SECRET_KEY = env('DJANGO_SECRET_KEY')


class SignupView(APIView):
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
                    "message": "회원가입에 성공했습니다!",
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
                        "message": "로그인에 성공했습니다!",
                        "token": {
                            "access": access_token,
                            "refresh": refresh_token,
                        },
                    },
                    status=status.HTTP_200_OK
                )
                return res

            else:
                return Response({'message': '비밀번호가 틀렸습니다!'}, status=status.HTTP_401_UNAUTHORIZED)

        elif user is None:
                return Response({'message': '유저 정보가 존재하지 않습니다!'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'message': '로그인에 실패했습니다!'}, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    def post(self, request):
        try:
            refresh = RefreshToken(request.data.get('refresh'))
            refresh.blacklist()
            return Response({"message": "로그아웃 완료"})
        except Exception:
            return Response({"message": "로그아웃이 불가한 상태입니다."})
            

class UserView(generics.GenericAPIView):
    def get(self, request):
        try:
            header_authorization = request.headers.get('Authorization', None)
            access = jwt.decode(header_authorization, SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=access["user_id"])
        except jwt.exceptions.ExpiredSignatureError:
            return Response({'message': '미 로그인 상태'}, status=status.HTTP_401_UNAUTHORIZED)

        if user.is_authenticated:
            return Response({'username': user.username, 'message': '로그인 상태'}, status=status.HTTP_200_OK)

class CandidateView(APIView):
    def get(self, request):  # 후보자 현황 가져오기
        candidates = Candidate.objects.all().order_by('-vote_cnt')
        serializer = CandidateSerializer(candidates, many=True)
        return Response(serializer.data)

class VoteView(APIView):
    def post(self, request):
        try:
            header_authorization = request.headers.get('Authorization', None)
            access = jwt.decode(header_authorization, SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=access["user_id"])

        except jwt.exceptions.ExpiredSignatureError:
            return Response({'message': '투표는 로그인이 필요합니다!'}, status=status.HTTP_401_UNAUTHORIZED)

        if user.is_authenticated:
            candidate_name = self.request.data['candidate']
            candidate = Candidate.objects.get(candidate_name=candidate_name)

            if not user.voted_be:  # 아직 투표하지 않은 투표자라면
                candidate.vote_cnt = candidate.vote_cnt + 1
                candidate.save()
                user.voted_be = True
                user.save()
                return JsonResponse({
                    'message': '투표가 완료됐습니다!',
                    'user_name': user.username,
                    'candidate_name': candidate_name,
                    'vote_cnt': candidate.vote_cnt}, status=HTTP_201_CREATED)
            else:  # 이미 투표를 했다면 투표권 X
                return JsonResponse({'message': '투표는 1회만 가능합니다!'}, status=status.HTTP_401_UNAUTHORIZED)