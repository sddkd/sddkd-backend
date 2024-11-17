from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import UserDetailsSerializer
from django.contrib.auth.models import User
from django.db import transaction
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Interest, UserProfile


class CustomRegisterSerializer(RegisterSerializer):
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])

    def save(self, request):
        with transaction.atomic():
            user = super().save(request)
            user_profile = UserProfile.objects.create(user=user)
            if request.data.get('profile'):
                serializer = UserProfileSerializer(instance=user_profile, data=request.data['profile'])
                if serializer.is_valid():
                    serializer.save()
        return user


class CustomUserDetailsSerializer(UserDetailsSerializer):
    profile = serializers.SerializerMethodField()

    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + ('profile',)

    def get_profile(self, obj):
        return UserProfileSerializer(obj.profile).data


class UserProfileSerializer(serializers.ModelSerializer):
    # date_of_birth = serializers.DateField(required=False)
    # interests = serializers.PrimaryKeyRelatedField(many=True)
    # interests = serializers.PrimaryKeyRelatedField(queryset=Interest.objects.all(), many=True)

    class Meta:
        model = UserProfile
        fields = ['date_of_birth', 'skill_level', 'interests']

    # def update(self, instance, validated_data):
    #     interests_data = validated_data.pop('interests', None)
    #     instance = super().update(instance, validated_data)
    #     if interests_data is not None:
    #         instance.interests.set(interests_data)
    #     return instance

