from django.http import HttpResponse
from rest_framework import serializers
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from dj_rest_auth.views import UserDetailsView

from .models import Interest, UserProfile
from .serializers import UserProfileSerializer


# class CustomUserDetailsView(UserDetailsView):
#     def patch(self, request, *args, **kwargs):
#         if request.data.get('profile'):
#             user_profile = UserProfile.objects.get(user=self.request.user)
#             serializer = UserProfileSerializer(instance=user_profile, data=request.data['profile'])
#             if serializer.is_valid():
#                 serializer.save()
#         return super().patch(request, *args, **kwargs)


class UserApiView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        user_profile = UserProfile.objects.get(user=request.user)
        if not user_profile:
            return Response(
                {"res": "Object with user id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = UserProfileSerializer(instance=user_profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InterestApiView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        interests = Interest.objects.all()
        return Response(interests.values('name'), status=status.HTTP_200_OK)


def index(request):
    return HttpResponse("Hello, world.")
