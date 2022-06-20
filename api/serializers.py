from rest_framework import serializers

from .models import *

# 사용자 정보 추출
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

# 회원가입
class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'], # 아이디
            password=validated_data['password'], # 비밀번호
            email=validated_data['email'], # 메일주소
        )
        user.save()
        return user

# 후보자 정보 추출
class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = '__all__'
