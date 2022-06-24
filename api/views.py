from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from .models import *
from rest_framework import viewsets, permissions, generics, status
from .serializer import *
from knox.models import AuthToken
from django.shortcuts import get_object_or_404
from django.http import JsonResponse


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


class CandidateApi(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self,request):
        candidates = Candidate.objects.all().order_by('-count')
        serializer = CandidateSerializer(candidates, many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer = CandidateSerializer(request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        serializer.save()
        JsonResponse({
            "message" : "successfully created"
        }, status=status.HTTP_201_CREATED)


class VoteApi(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        candidates = Candidate.objects.all()
        serializer = CandidateSerializer(candidates,many=True)
        return Response(serializer.data)

    def post(self, request):
        user = get_object_or_404(User, pk=request.user.id)
        candidate_id = request.data['candidate']

        candidate = get_object_or_404(Candidate, pk=candidate_id)

        data = {'candidate': candidate.id, 'user': user.id}
        vote_serializer = VoteSerializer(data=data)
        if not vote_serializer.is_valid():
            JsonResponse(
                vote_serializer.errors,status.HTTP_400_BAD_REQUEST
            )
        if user.voteChecker :
            JsonResponse({
                "message": "you did it."
            }, status.HTTP_400_BAD_REQUEST)

        candidate.count+=1
        candidate.save();
        user.voteChecker=True
        user.save()
        vote_serializer.save()

        return JsonResponse({
            "message" : "thank you for your voting"
        }, status.HTTP_201_CREATED)






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
