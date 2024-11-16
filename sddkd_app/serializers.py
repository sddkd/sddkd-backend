from dj_rest_auth.registration.serializers import RegisterSerializer
from django.contrib.auth.models import User
from django.db import transaction
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import UserProfile


class CustomRegisterSerializer(RegisterSerializer):
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])
    date_of_birth = serializers.DateField(required=False)

    def save(self, request):
        with transaction.atomic():
            user = super().save(request)
            UserProfile.objects.create(user=user, date_of_birth=self.validated_data.get('date_of_birth'))
        return user
