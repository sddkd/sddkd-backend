from datetime import date

from django.conf import settings
from django.db import models


class UserProfile(models.Model):
    class SkillsLevels(models.TextChoices):
        BEGINNER = "beginner", "Beginner"
        INTERMEDIATE = "intermediate", "Intermediate"
        PRO = "pro", "Pro"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile"
    )
    date_of_birth = models.DateField()
    skill_level = models.CharField(choices=SkillsLevels, default=SkillsLevels.BEGINNER)
    time_requirements = models.TimeField()
    topics = models.ManyToManyField("Topic")
    tasks = models.ManyToManyField("Task", through="UsersTasks")

    def __str__(self):
        return self.user.username

    @property
    def age(self):
        today = date.today()
        age = today.year - self.date_of_birth.year
        if (today.month, today.day) < (
            self.date_of_birth.month,
            self.date_of_birth.day,
        ):
            age -= 1
        return age


class Topic(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField()

    def __str__(self):
        return self.name


class Task(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField()
    time_requirements = models.TimeField()
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class UsersTasks(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    started_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user} - {self.task}"

    @property
    def time_spent(self):
        if self.started_at and self.finished_at:
            return self.finished_at - self.started_at
        return None


class Post(models.Model):
    user = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="posts"
    )
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    hashtag_list = models.CharField(null=True, blank=True)
    image_base64 = models.TextField()

    @property
    def likes_counter(self):
        return self.likes.count()


class PostLike(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "post")


class Notification(models.Model):
    user = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="notifications"
    )
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
