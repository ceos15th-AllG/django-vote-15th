from rest_framework import serializers
from .models import User, Vote, Candidate
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'voteChecker']


class SignUpSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            username=validated_data['username'],
        )
        user.set_password(validated_data['password'])

        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    email = serializers.EmailField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("login error")


class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = ['count', 'name', 'image', 'content']


class VoteSerializer(serializers.ModelSerializer):
    voter_name = UserSerializer(many=False, read_only=True)
    candidate_name = CandidateSerializer(many=True)

    class Meta:
        model = Vote
        fields = ['voter_name', 'candidate_name']
