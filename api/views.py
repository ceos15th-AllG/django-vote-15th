from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from .models import *
from rest_framework import viewsets, permissions, generics, status
from .serializer import *
from knox.models import AuthToken


class SignUpApi(generics.GenericAPIView):
    serializer_class = SignUpSerializer

    def post(self, request, *args, **kwargs):
        if len(request.data["username"]) < 3 or len(request.data["password"]) < 4:
            body = {"message": "too short"}
            return Response(body, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                "user": UserSerializer(
                    user, context=self.get_serializer_context()
                ).data,
                "token": AuthToken.objects.create(user)[1],
            }
        )


class LoginApi(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response(
            {
                "user": UserSerializer(user, context=self.get_serializer_context()).data,
                "token ": AuthToken.objects.create(user)[1],
            }
        )


class UserApi(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class CandidateListApi(generics.RetrieveAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer


#
# class MemberViewSet(ModelViewSet):
#     serializer_class = MemberSerializer
#     queryset = Member.objects.all()
#
#
# class CandidateViewSet(ModelViewSet):
#     queryset = Candidate.objects.all()
#     serializer_class = CandidateSerializer
#
#
# class VoteViewSet(ModelViewSet):
#     queryset = Vote.objects.all()
#     serializer_class = VoteSerializer
