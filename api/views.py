from django_filters.rest_framework import FilterSet, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins, exceptions, permissions
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from api.serializers import *


class CandidateFilter(FilterSet):
    part = filters.CharFilter(method='filter_by_part')

    class Meta:
        model = Candidate
        fields = ['user_name']

    def filter_by_part(self, queryset, name, value):
        filtered_queryset = queryset.filter(part=value)
        return filtered_queryset


class CandidateViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = CandidateSerializer
    queryset = Candidate.objects.all().order_by('-vote_count')
    filter_backends = [DjangoFilterBackend]
    filterset_class = CandidateFilter


class VotePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        else:
            return True # 유저 구현 후 request.user.is_authenticated로 변경 필요


class VoteViewSet(viewsets.ModelViewSet):
    serializer_class = VoteSerializer
    queryset = Vote.objects.all().order_by('-created_at')
    permission_classes = [VotePermission, ]

    def perform_create(self, serializer):
        candidate_id = self.request.data['candidate']
        user_id = self.request.data['user']
        check_vote = Vote.objects.filter(candidate_id=candidate_id, user_id=user_id)
        if len(check_vote) != 0:
            raise exceptions.ValidationError(detail='해당 유저는 해당 후보에 이미 투표한 상태입니다.')
        else:
            candidate = Candidate.objects.get(id=candidate_id)
            candidate.vote_count = candidate.vote_count + 1
            candidate.save()
            serializer.save()


class SignUpView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = JSONParser().parse(self.request)
        serializer = SignUpSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            res_data = SignInSerializer.user_login(None, data)
            return Response(res_data, status=201)
        return Response(serializer.errors, status=400)


class SignInView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = JSONParser().parse(self.request)

        res_data = SignInSerializer.user_login(None, data)
        return Response(res_data, status=200)
