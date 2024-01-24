from django.contrib.auth.models import User
from django.http import Http404, JsonResponse
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404

from userprofile.models import Profile
from userprofile.serializers import ProfileSerializer, UserCreateSerializer


class UserCreateAPIView(ListCreateAPIView):
    serializer_class = UserCreateSerializer
    authentication_classes = ([])
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        if request.user is not None:
            user_data = {'username': request.data.get('username'), 'password': request.data.get('password')}

            user_serializer = UserCreateSerializer(data=user_data)

            if user_serializer.is_valid():
                User.objects.create_user(username=user_data['username'], password=user_data['password'])
                return Response(user_serializer.data, status=status.HTTP_201_CREATED)

            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileAPIView(ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProfileSerializer

    def get_queryset(self):
        user = self.request.user
        return Profile.objects.get(user__id=user.id)

    def get(self, request, *args, **kwargs):
        user_profile = get_object_or_404(Profile, user=request.user)
        serializer = ProfileSerializer(user_profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        if request.user is not None:
            user_profile_data = {'jobTitle': request.data.get('jobTitle'),
                                 'company': request.data.get('company'),
                                 'first_name': request.data.get('first_name'),
                                 'last_name': request.data.get('last_name')}

            user_profile_serializer = ProfileSerializer(data=user_profile_data)

            if user_profile_serializer.is_valid():
                user_profile_serializer.validated_data['user'] = request.user
                user = User.objects.get(id=request.user.id)
                user.first_name = request.data['first_name']
                user.last_name = request.data['last_name']
                user.save()
                user_profile_serializer.validated_data['user'].first_name = request.data['first_name']
                user_profile_serializer.validated_data['user'].last_name = request.data['last_name']
                user_profile_serializer.save()
                return Response(user_profile_serializer.data, status=status.HTTP_201_CREATED)

            return Response(user_profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def getuserid(request, username):
    user = User.objects.get(username=username)
    if user:
        return JsonResponse({'id': user.id})
    else:
        return Http404
