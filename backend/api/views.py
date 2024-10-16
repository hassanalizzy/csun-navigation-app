from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Building, Room, Schedule
from .serializers import (
    UserSerializer,
    BuildingSerializer,
    RoomSerializer,
    ScheduleSerializer,
)
from rest_framework import status

# User registration
@api_view(['POST'])
def register_user(request):
    # Your existing code remains the same
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')

    # Checks if the username already exists
    if User.objects.filter(username=username).exists():
        return Response(
            {'error': 'Username already exists'},
            status=status.HTTP_400_BAD_REQUEST
        )

    User.objects.create_user(
        username=username, email=email, password=password
    )
    return Response(
        {'message': 'User registered successfully'},
        status=status.HTTP_201_CREATED
    )

# User authentication/login
@api_view(['POST'])
def login_user(request):
    # Your existing code remains the same
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    if user:
        login(request, user)
        return Response(
            {'message': 'User logged in successfully'},
            status=status.HTTP_200_OK
        )
    else:
        return Response(
            {'error': 'Invalid credentials'},
            status=status.HTTP_400_BAD_REQUEST
        )

# User logout
@api_view(['POST'])
def logout_user(request):
    # Your existing code remains the same
    logout(request)
    return Response(
        {'message': 'User logged out successfully'},
        status=status.HTTP_200_OK
    )

# Get list of buildings
@api_view(['GET'])
def buildings(request):
    buildings = Building.objects.all()
    serializer = BuildingSerializer(buildings, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# Get list of rooms filtered by building and optional floor
@api_view(['GET'])
def rooms(request):
    building_id = request.GET.get('building_id')
    floor_number = request.GET.get('floor_number')

    if not building_id:
        return Response(
            {'error': 'Building ID is required.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    rooms = Room.objects.filter(building_id=building_id)
    if floor_number:
        rooms = rooms.filter(floor_number=floor_number)

    serializer = RoomSerializer(rooms, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# Save schedule
@api_view(['POST'])
def save_schedule(request):
    user = request.user
    if not user.is_authenticated:
        return Response(
            {'error': 'User not authenticated'},
            status=status.HTTP_401_UNAUTHORIZED
        )

    class_name = request.data.get('class_name')
    class_number = request.data.get('class_number')
    room_id = request.data.get('room_id')

    if not all([class_name, class_number, room_id]):
        return Response(
            {'error': 'Class name, class number, and room ID are required.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        room = Room.objects.get(id=room_id)
    except Room.DoesNotExist:
        return Response(
            {'error': 'Invalid room ID'},
            status=status.HTTP_400_BAD_REQUEST
        )

    schedule = Schedule.objects.create(
        user=user,
        class_name=class_name,
        class_number=class_number,
        room=room
    )

    return Response(
        {'message': 'Schedule saved successfully'},
        status=status.HTTP_201_CREATED
    )

# Get user's schedule
@api_view(['GET'])
def get_schedule(request):
    user = request.user
    if not user.is_authenticated:
        return Response(
            {'error': 'User not authenticated'},
            status=status.HTTP_401_UNAUTHORIZED
        )

    schedules = Schedule.objects.filter(user=user)
    serializer = ScheduleSerializer(schedules, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
