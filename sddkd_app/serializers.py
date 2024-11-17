from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import UserDetailsSerializer
from django.contrib.auth.models import User
from django.db import transaction
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Notification, Post, PostLike, Task, Topic, UserProfile, UsersTasks


class CustomRegisterSerializer(RegisterSerializer):
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])

    def save(self, request):
        with transaction.atomic():
            user = super().save(request)
            data = {'user': user.id}
            if request.data.get('profile'):
                data |= request.data['profile']
                serializer = UserProfileSerializer(data=data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
        return user


class CustomUserDetailsSerializer(UserDetailsSerializer):
    profile = serializers.SerializerMethodField()

    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + ('profile',)

    def get_profile(self, obj):
        return UserProfileSerializer(obj.profile).data


class UserProfileSerializer(serializers.ModelSerializer):
    tasks = serializers.SerializerMethodField()
    age = serializers.SerializerMethodField()
    posts = serializers.SerializerMethodField()
    notifications = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = '__all__'

    def validate_interests(self, value):
        interests_limit = 3
        if len(value) > interests_limit:
            raise serializers.ValidationError(f'You can only have up to {interests_limit} topics.')
        return value

    def get_tasks(self, obj):
        users_tasks = UsersTasks.objects.filter(user=obj)
        return UsersTasksSerializer(users_tasks, many=True).data

    def get_age(self, obj):
        return obj.age

    def get_posts(self, obj):
        return PostSerializer(obj.posts.all(), many=True).data

    def get_notifications(self, obj):
        return NotificationSerializer(obj.notifications.all(), many=True).data


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class UsersTasksSerializer(serializers.ModelSerializer):
    task = TaskSerializer()
    time_spent = serializers.SerializerMethodField()

    class Meta:
        model = UsersTasks
        fields = '__all__'

    def get_time_spent(self, obj):
        return obj.time_spent


class PostSerializer(serializers.ModelSerializer):
    task = TopicSerializer()
    likes_counter = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'

    def get_likes_counter(self, obj):
        return obj.likes_counter


class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = '__all__'


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
