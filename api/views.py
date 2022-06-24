import generics as generics

from .serializers import *
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.http import Http404
from rest_framework.permissions import IsAuthenticated


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class SignUpAPIView(APIView):
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            token = RefreshToken.for_user(user)

            return Response({
                "user": user.username,
                "message": "Sign up Success",
                "refresh": str(token),
                "access": str(token.access_token),
            })

        else:
            return Response(serializer.errors)


class LoginAPIView(APIView):
    def post(self, request):
        username = request.data.get('username', None)
        password = request.data.get('password', None)
        user = authenticate(username=username, password=password)

        if user is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            token = RefreshToken.for_user(user)

            return Response(
                {
                    "user": user.username,
                    "message": "Login Success",
                    "refresh": str(token),
                    "access": str(token.access_token),
                }
            )


class CandidateList(APIView):
    def get_object(self, part):
        try:
            return Candidate.objects.get(part=part)
        except Candidate.DoesNotExist:
            raise Http404

    def get(self, request, part, format=None):
        candidates = Candidate.objects.filter(part=part)
        serializer = CandidateSerializer(candidates, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CandidateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CandidateDetail(APIView):
    permissions_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Candidate.objects.get(pk=pk)
        except Candidate.DoesNotExist:
            raise Http404

    def get(self, request, part, pk, format=None):
        candidate = self.get_object(pk)
        vote = {'vote_num': candidate.vote_num+1}
        serializer = CandidateSerializer(candidate, data=vote, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TestAPIView(APIView):
    def get(self, request):
        return Response({"test": "success"})