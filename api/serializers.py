from rest_framework import serializers
from api.models import *


class VoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vote
        fields = ['id', 'candidate', 'user']


class CandidateSerializer(serializers.ModelSerializer):
    candidate_votes = VoteSerializer(many=True, read_only=True)

    class Meta:
        model = Candidate
        fields = '__all__'
