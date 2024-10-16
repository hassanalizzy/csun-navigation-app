from django.contrib import admin
from .models import Building, Room, Schedule

admin.site.register(Building)
admin.site.register(Room)
admin.site.register(Schedule)
