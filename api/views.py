from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .serializers import *
from .models import *
from rest_framework import viewsets, views, permissions, exceptions
from rest_framework.status import *
from rest_framework.response import Response


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class SignUpView(views.APIView):
    serializer_class = SignUpSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            token = RefreshToken.for_user(user)
            refresh = str(token)
            access = str(token.access_token)

            return JsonResponse({
                'message': 'Signup Success',
                'user': user.username,
                'access': access,
                'refresh': refresh,
            }, status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class LoginView(views.APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = serializer.validated_data['refresh']
            access = serializer.validated_data['access']

            return JsonResponse({
                'message': 'Login Success',
                'user': user.username,
                'access': access,
                'refresh': refresh,
                'is_voted': user.is_voted,
            }, status=HTTP_200_OK)

        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class VoteListView(views.APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        candidates = Candidate.objects.all().order_by('-count')  # 내림차순
        serializer = CandidateSerializer(candidates, many=True)

        return Response(serializer.data, status=HTTP_200_OK)

    def post(self, request):
        user = get_object_or_404(User, pk=request.user.id)
        candidate_id = request.data['candidate']

        if not candidate_id:
            return JsonResponse({'message': 'Invalid candidate'}, status=HTTP_400_BAD_REQUEST)

        candidate = get_object_or_404(Candidate, pk=candidate_id)

        data = {'candidate': candidate.id, 'user': user.id}
        vote_serializer = VoteSerializer(data=data)

        if not vote_serializer.is_valid():
            return Response(vote_serializer.errors, status=HTTP_400_BAD_REQUEST)
        if user.is_voted:
            return JsonResponse({'message': 'You have already voted'}, status=HTTP_409_CONFLICT)

        candidate.count += 1
        candidate.save()
        #user.is_voted = True
        user.save()
        vote_serializer.save()

        return JsonResponse({
            'message': 'Successfully Voted',
            'user': user.username,
            'is_voted': user.is_voted}, status=HTTP_201_CREATED)


class VoteDetailView(views.APIView):
    def get_object(self, pk):
        return get_object_or_404(Candidate, pk=pk)

    def get(self, request, pk):
        candidate = self.get_object(pk)
        serializer = CandidateSerializer(candidate)

        return Response(serializer.data, status=HTTP_200_OK)


class CandidateView(views.APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def post(self, request):
        serializer = CandidateSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

        name = serializer.validated_data['name']

        if Candidate.objects.filter(name=name).exists():
            return exceptions.ParseError()

        serializer.save()
        return JsonResponse({
            'message': 'Successfully Created',
            'id': serializer.data['id'],
            'name': serializer.data['name'],
            'count': serializer.data['count'],
        }, status=HTTP_201_CREATED)