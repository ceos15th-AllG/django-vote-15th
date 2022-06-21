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
    permission_classes = [AllowAny]

    def get(self, request):
        part = request.query_params.get('part', None)
        if part != 'BE' and part != 'FE':
            raise exceptions.ValidationError(detail='검색하고자 하는 파트를 명확하게 입력해주세요')
        candidates = Candidate.objects.filter(part=part).order_by('-vote_count', 'user_name')
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


    def post(self, request):
        candidate_id = request.data['candidate']
        token_user = request.user
        bearer = request.headers['Authorization']
        token = bearer.split()
        print(token[1])
        token_user_id = MyUser.objects.get(email=token_user)
        if token_user_id.id is None:
            raise exceptions.ValidationError(detail='유저 정보를 확인해 주세요.')
        elif token_user_id.denied_access_token == token[1]:
            raise exceptions.AuthenticationFailed(detail='토큰이 만료되었습니다.')
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
        print(data)
        res_data = SignInSerializer.user_login(None, data)
        return Response(generate_success_form(200, '로그인 성공', res_data), status=200)


class RefreshTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            header_token = request.headers['Refresh-Authorization']
            print(header_token)
            user = MyUser.objects.get(refresh_token=header_token)
            payload = jwt.decode(header_token, settings.SECRET_KEY, algorithms=['HS256'])
            get_user = MyUser.objects.get(id=payload['user_id'])
            jwt_token = TokenObtainPairSerializer.get_token(get_user)
            access_token = str(jwt_token.access_token)
            return Response(generate_success_form(200, '토큰 재발급 성공', {
                'access_token': access_token
            }))
        except MyUser.DoesNotExist:
            raise exceptions.NotAuthenticated(detail='토큰 재발급 권한이 없습니다.')
        except jwt.ExpiredSignatureError:
            user.refresh_token = ''
            user.save()
            raise exceptions.AuthenticationFailed(detail='리프레쉬 토큰 만료')


class LogoutView(APIView):
    permission_classes = [VotePermission]

    def post(self, request):
        try:
            user = request.user
            bearer = request.headers['Authorization']
            token = bearer.split()
            if user.denied_access_token == token[1]:
                raise exceptions.AuthenticationFailed(detail='이미 로그아웃된 계정입니다.')
            user = MyUser.objects.get(id=user.id)
            user.refresh_token = ''
            user.denied_access_token = token[1]
            user.save()
            return Response(generate_success_form(200, '로그아웃 성공', {}), status=200)
        except MyUser.DoesNotExist:
            raise exceptions.ValidationError(detail='토큰 정보를 확인해주세요')

