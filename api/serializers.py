from rest_framework import serializers
from api.models import *
from django.contrib.auth.hashers import *


class SignUpSerializer(serializers.ModelSerializer):
    # user_name = serializers.CharField(required=True)
    # email = serializers.EmailField(required=True)
    # password = serializers.CharField(required=True)
    # part = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['user_name', 'email', 'password', 'part']

    def create(self, validated_data):
        if len(validated_data['password']) > 15 or len(validated_data['password']) < 8:
            raise serializers.ValidationError("비밀번호는 8자 이상, 15자 이하입니다.", code=400)
        password = make_password(validated_data['password'])
        user = User.objects.create(
            user_name=validated_data['user_name'],
            password=password,
            email=validated_data['email'],
            part=validated_data['part']
        )
        user.save()
        return user


class VoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vote
        fields = ['id', 'candidate', 'user']


class CandidateSerializer(serializers.ModelSerializer):
    candidate_votes = VoteSerializer(many=True, read_only=True)

    class Meta:
        model = Candidate
        fields = '__all__'

