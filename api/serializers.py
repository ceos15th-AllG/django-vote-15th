from rest_framework import serializers

from api.models import Voter


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voter
        fields = ['username', 'id', 'password', 'email']

    def create(self, validated_data):
        voter = Voter.objects.create(
            username=validated_data['username'], # 아이디
            password=validated_data['password'], # 비밀번호
            email=validated_data['email'], # 메일주소
        )
        voter.save()
        return voter
