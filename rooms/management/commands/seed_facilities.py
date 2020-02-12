from django.core.management.base import BaseCommand
from rooms.models import Facility

# = from rooms import models as room_models


class Command(BaseCommand):
    help = "This command creates amenity objects."

    def handle(self, *args, **options):
        facilities = [
            "Private entrance",
            "Paid parking on premises",
            "Paid parming off premises",
            "Elevator",
            "Parking",
            "Gym",
        ]
        
        if Facility.objects.count() == 0:
            for f in facilities:
                Facility.objects.create(name=f)
            self.stdout.write(self.style.SUCCESS(f"{len(facilities)} facilities created!"))
        else:
            self.stdout.write(self.style.SUCCESS("facilities exist!"))
        # times = options.get("times")
        # for t in range(0, int(times)):
        #     self.stdout.write(self.style.NOTICE("heyhey!\n"))
