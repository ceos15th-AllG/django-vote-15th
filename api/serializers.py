from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer

from api.models import *
from django.contrib.auth.hashers import *


class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = MyUser
        fields = ['name', 'email', 'password', 'part']

    def create(self, validated_data):
        if len(validated_data['password']) > 15 or len(validated_data['password']) < 8:
            raise serializers.ValidationError("비밀번호는 8자 이상, 15자 이하입니다.", code=400)
        password = make_password(validated_data['password'])
        user = MyUser.objects.create(
            name=validated_data['name'],
            password=password,
            email=validated_data['email'],
            part=validated_data['part'],
        )
        user.save()
        return user

    def auto_login(self, data):
        email = data.get('email')
        user = MyUser.objects.get(email=email)

        jwt_token = TokenObtainPairSerializer.get_token(user)
        access_token = str(jwt_token.access_token)

        return {
            'name': user.name,
            'email': user.email,
            'part': user.part,
            'token': {
                'access_token': access_token,
            }
        }


class SignInSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = MyUser
        fields = ['name', 'email', 'password', 'token']

    def user_login(self, data):
        email = data.get("email", None)
        password = data.get("password", None)
        user = MyUser.objects.get(email=email)

        if user is None or check_password(password, user.password) is False:
            raise serializers.ValidationError('아이디 또는 비밀번호가 틀렸습니다.', code=400)
        else:
            jwt_token = TokenObtainPairSerializer.get_token(user)
            access_token = str(jwt_token.access_token)

            return {
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'part': user.part,
                'token': {
                    'access_token': access_token,
                }
            }


class VoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vote
        fields = ['id', 'candidate', 'user']


class CandidateSerializer(serializers.ModelSerializer):
    candidate_votes = VoteSerializer(many=True, read_only=True)

    class Meta:
        model = Candidate
        fields = '__all__'

