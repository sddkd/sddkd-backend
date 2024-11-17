from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny
from rest_framework.routers import DefaultRouter

from .views import (
    NotificationViewSet, PostLikeViewSet, PostViewSet, TaskViewSet,
    TopicViewSet, UserApiView, UsersTasksViewSet,
)

router = DefaultRouter()
router.register('topics', TopicViewSet, basename='topic')
router.register('tasks', TaskViewSet, basename='task')
router.register('users-tasks', UsersTasksViewSet, basename='user-task')
router.register('posts', PostViewSet, basename='post')
router.register('posts-likes', PostLikeViewSet, basename='post-like')
router.register('notifications', NotificationViewSet, basename='notification')

# Swagger/OpenAPI schema view
schema_view = get_schema_view(
    openapi.Info(
        title='SDDKD API',
        default_version='v1',
        description='API documentation',
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email='frontend@example.com'),
        license=openapi.License(name='MIT License'),
    ),
    public=True,
    permission_classes=[AllowAny],
    authentication_classes=[],
)

urlpatterns = [
    path('', include(router.urls)),
    path('users/', UserApiView.as_view()),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
