from django.db import models
from django.contrib.auth.models import User

class Building(models.Model):
    name = models.CharField(max_length=100)
    floors = models.IntegerField()  # Number of floors in the building
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name

class Room(models.Model):
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='rooms')
    floor_number = models.IntegerField()
    room_number = models.CharField(max_length=10)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return f"{self.building.name} Floor {self.floor_number} Room {self.room_number}"

class Schedule(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    class_number = models.CharField(max_length=20)
    class_name = models.CharField(max_length=100)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}'s {self.class_name} ({self.class_number}) in {self.room}"

# Create your models here.
