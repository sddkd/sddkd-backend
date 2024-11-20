from django_filters import rest_framework as filters

from sddkd_app.models import Post


class PostFilter(filters.FilterSet):
    user_id = filters.NumberFilter(field_name='user__id')

    class Meta:
        model = Post
        fields = ['user_id']
