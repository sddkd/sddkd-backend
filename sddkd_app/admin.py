from django.contrib import admin

from .models import Notification, Post, PostLike, Task, Topic, UserProfile, UsersTasks

admin.site.register(UserProfile)
admin.site.register(Topic)
admin.site.register(Task)
admin.site.register(UsersTasks)
admin.site.register(Post)
admin.site.register(PostLike)
admin.site.register(Notification)
