from django_filters.rest_framework import FilterSet, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins
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
    queryset = Candidate.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = CandidateFilter

