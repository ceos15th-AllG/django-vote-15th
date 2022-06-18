import environ
import jwt
from django_filters.rest_framework import FilterSet, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins, exceptions, permissions
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from api.serializers import *

env = environ.Env(
    DEBUG = (bool, False)
)


def generate_success_form(code, message, detail):
    return {
        'status': code,
        'message': message,
        'detail': detail
    }


class CandidateView(APIView):

    def get(self, request):
        part = request.query_params.get('part', None)
        if part != 'BE' and part != 'FE':
            raise exceptions.ValidationError(detail='검색하고자 하는 파트를 명확하게 입력해주세요')
        candidates = Candidate.objects.filter(part=part)
        serializer = CandidateSerializer(candidates, many=True)

        return Response(generate_success_form(200, '검색 성공', serializer.data), status=200)


class VotePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        else:
            return request.user.is_authenticated


class VoteView(APIView):
    permission_classes = [VotePermission]

    def post(self, request, pk):
        candidate_id = pk
        token_user = request.user
        token_user_id = MyUser.objects.get(name=token_user).id
        check_vote = Vote.objects.filter(candidate_id=candidate_id, user_id=token_user_id)

        if len(check_vote) != 0:
            raise exceptions.ValidationError(detail='해당 유저는 해당 후보에 이미 투표한 상태입니다.')
        else:
            candidate = Candidate.objects.get(id=candidate_id)
            candidate.vote_count = candidate.vote_count + 1
            candidate.save()
            vote_serializer = VoteSerializer(data={
                'candidate': candidate_id,
                'user': token_user_id
            })
            if vote_serializer.is_valid(raise_exception=True):
                vote_serializer.save()
                res_data = {
                    'user': token_user_id,
                    'candidate': candidate_id
                }
                return Response(generate_success_form(201, '투표 성공', res_data), status=201)
            return Response(vote_serializer.errors, status=400)


class SignUpView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = JSONParser().parse(self.request)
        serializer = SignUpSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            res_data = SignInSerializer.user_login(None, data)
            return Response(generate_success_form(201, '회원가입 성공', res_data), status=201)
        return Response(serializer.errors, status=400)


class SignInView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = JSONParser().parse(self.request)

        res_data = SignInSerializer.user_login(None, data)
        return Response(generate_success_form(200, '로그인 성공', res_data), status=200)
