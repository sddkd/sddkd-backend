from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import PostFilter
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

    @action(detail=False, methods=['get'], url_path='current-user')
    def current_user_tasks(self, request):
        user = request.user.profile
        queryset = self.queryset.filter(user=user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PostFilter

    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'], url_path='random')
    def current_user_tasks(self, request):
        queryset = self.queryset.order_by('?')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PostLikeViewSet(viewsets.ModelViewSet):
    queryset = PostLike.objects.all()
    serializer_class = PostLikeSerializer

    http_method_names = ['get', 'post', 'delete']
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if PostLike.objects.filter(post=request.data['post'], user=request.user.profile).exists():
            return Response({'error': 'You have already liked this post.'}, status=status.HTTP_400_BAD_REQUEST)

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
