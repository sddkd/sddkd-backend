from django.urls import path

from . import views
from .views import InterestApiView, UserApiView

urlpatterns = [
    path('', views.index, name='index'),
    path('interests', InterestApiView.as_view()),
    path('users/', UserApiView.as_view()),
]
