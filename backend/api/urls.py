from django.urls import path
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Building, Room, Schedule
from .serializers import UserSerializer, RoomSerializer, ScheduleSerializer
from rest_framework import status
from . import views

urlpatterns = [
    path('register/', views.register_user),
    path('login/', views.login_user),
    path('logout/', views.logout_user),
    path('buildings/', views.buildings),
    path('rooms/', views.rooms),
    path('save_schedule/', views.save_schedule),
    path('get_schedule/', views.get_schedule),
]

