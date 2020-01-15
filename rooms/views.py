from django.shortcuts import render
from . import models

# from django.http import HttpResponse


def all_rooms(request):
    # print(dir(request))

    # Don't use this way ever! This will kill your DB.
    all_rooms = models.Room.objects.all()

    return render(request, "rooms/all_rooms.html", context={"rooms": all_rooms})
