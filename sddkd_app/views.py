from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Notification, Post, PostLike, Task, Topic, UserProfile, UsersTasks
from .serializers import (
    NotificationSerializer, PostLikeSerializer, PostSerializer, TaskSerializer, TopicSerializer, UserProfileSerializer,
    UsersTasksSerializer,
)


class UserApiView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        user_profile = UserProfile.objects.get(user=request.user)
        if not user_profile:
            return Response(
                {'res': 'Object with user id does not exists'},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = UserProfileSerializer(instance=user_profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

    http_method_names = ['get']
    authentication_classes = []
    permission_classes = [AllowAny]


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    permission_classes = [IsAuthenticated]


class UsersTasksViewSet(viewsets.ModelViewSet):
    queryset = UsersTasks.objects.all()
    serializer_class = UsersTasksSerializer

    permission_classes = [IsAuthenticated]


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    permission_classes = [IsAuthenticated]


class PostLikeViewSet(viewsets.ModelViewSet):
    queryset = PostLike.objects.all()
    serializer_class = PostLikeSerializer

    http_method_names = ['get', 'post', 'delete']
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        like = serializer.save()
        response_data = {
            'post_id': like.post.id,
            'likes_counter': like.post.likes_counter
        }
        return Response(response_data, status=status.HTTP_201_CREATED)


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    permission_classes = [IsAuthenticated]
