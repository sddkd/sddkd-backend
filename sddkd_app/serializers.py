from dj_rest_auth.registration.serializers import RegisterSerializer
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class CustomRegisterSerializer(RegisterSerializer):
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])
    date_of_birth = serializers.DateField(required=False)

    def save(self, request):
        user = super().save(request)
        user.profile.date_of_birth = self.validated_data.get('date_of_birth')
        user.profile.save()
        return user
