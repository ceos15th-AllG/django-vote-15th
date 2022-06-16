from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from .serializers import *
from .models import *
from rest_framework import viewsets, views, permissions, exceptions
from rest_framework.status import *
from rest_framework.response import Response
import jwt
import environ

env = environ.Env(
    DEBUG=(bool, False)
)

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

            # request.session['access_token'] = access
            # request.session['refresh_token'] = refresh

            response = JsonResponse({
                'message': 'Signup Success',
                'user': user.username,
            }, status=HTTP_201_CREATED)

            response.set_cookie('access_token', access, domain='http://localhost:3000', httponly=False, samesite=None)
            response.set_cookie('refresh_token', refresh, domain='http://localhost:3000', httponly=False, samesite=None)

            return response

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

            # request.session['access_token'] = access
            # request.session['refresh_token'] = refresh

            response = JsonResponse({
                'message': 'Login Success',
                'user': user.username,
                'is_voted': user.is_voted,
            }, status=HTTP_200_OK)

            response.set_cookie('access_token', access, domain='http://localhost:3000', httponly=False, samesite=None)
            response.set_cookie('refresh_token', refresh, domain='http://localhost:3000', httponly=False, samesite=None)

            return response

        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class LogoutView(views.APIView):
    def post(self, request):
        # del request.session['access_token']
        # del request.session['refresh_token']

        response = JsonResponse({
            'message': 'Logout Success',
        }, status=HTTP_200_OK)

        response.delete_cookie('access_token', domain='http://localhost:3000')
        response.delete_cookie('refresh_token', domain='http://localhost:3000')

        return response


class VotePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            if request.COOKIES.get('access_token'):
                access = request.COOKIE['access_token']
                payload = jwt.decode(access, env('DJANGO_SECRET_KEY'), algorithms=['HS256'])
                user = get_object_or_404(User, pk=payload['user_id'])
                request.user = user
                return True
            else:
                return False


class VoteListView(views.APIView):
    permission_classes = [VotePermission]

    def get(self, request):
        candidates = Candidate.objects.all().order_by('-count')  # 내림차순
        serializer = CandidateSerializer(candidates, many=True)

        return Response(serializer.data, status=HTTP_200_OK)

    def post(self, request):
        user = get_object_or_404(User, pk=request.user.id)
        candidate_id = request.data['candidate']
        candidate = get_object_or_404(Candidate, pk=candidate_id)

        data = {'candidate': candidate.id, 'user': user.id}
        vote_serializer = VoteSerializer(data=data)

        if not vote_serializer.is_valid():
            return Response(vote_serializer.errors, status=HTTP_400_BAD_REQUEST)
        if user.is_voted:
            return JsonResponse({'message': 'You have already voted'}, status=HTTP_409_CONFLICT)

        candidate.count += 1
        candidate.save()
        user.is_voted = True
        user.save()
        vote_serializer.save()
        return JsonResponse({'message': 'Successfully Voted'}, status=HTTP_201_CREATED)


class VoteDetailView(views.APIView):
    def get_object(self, pk):
        return get_object_or_404(Candidate, pk=pk)

    def get(self, request, pk):
        candidate = self.get_object(pk)
        serializer = CandidateSerializer(candidate)

        return Response(serializer.data, status=HTTP_200_OK)


class CandidatePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            if request.COOKIES.get('access_token'):
                return True
            else:
                return False


class CandidateView(views.APIView):
    permission_classes = [CandidatePermission]

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
