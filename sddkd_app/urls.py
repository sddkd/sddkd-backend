from django.urls import path

from . import views
from .views import QuestionApiView

urlpatterns = [
    path('', views.index, name='index'),
    path('api', QuestionApiView.as_view()),
]
