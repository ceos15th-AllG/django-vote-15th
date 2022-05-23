from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class SignUpSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(username=validated_data['username'], email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()

        return user

    def validate(self, data):
        username = data.get('username', None)
        email = data.get('email', None)

        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("Exist user")

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Exist email")

        return data

