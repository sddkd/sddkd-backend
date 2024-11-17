from django.conf import settings
from django.db import models


class Interest(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    class SkillsLevels(models.TextChoices):
        BEGINNER = 'beginner', 'Beginner'
        INTERMEDIATE = 'intermediate', 'Intermediate'
        PRO = 'pro', 'Pro'

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    date_of_birth = models.DateField(null=True, blank=True)
    skill_level = models.CharField(choices=SkillsLevels, default=SkillsLevels.BEGINNER)
    interests = models.ManyToManyField(Interest, related_name='user_profiles')

    def __str__(self):
        return self.user.username
