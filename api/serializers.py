from rest_framework import serializers
from .models import *


class SignUpSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "password", "email"]

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            username=validated_data['username'],
        )
        user.set_password(validated_data['password'])

        user.save()
        return user

    def validate(self, data):
        email = data.get('email', None)
        username = data.get('username', None)

        # 이메일 중복 체크
        user_email = User.objects.filter(email=email)
        if user_email:
            raise serializers.ValidationError(
                "EMAIL ALREADY EXIST"
            )

        # 이름 중복 체크
        user_name = User.objects.filter(username=username)
        if user_name:
            raise serializers.ValidationError(
                "USERNAME ALREADY EXIST"
            )

        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']
