from django.core.management.base import BaseCommand
from django_seed import Seed
from users.models import User

# = from rooms import models as room_models


class Command(BaseCommand):
    help = "This command creates superuser."

    def handle(self, *args, **options):
        admin = User.objects.get_or_none(username="mybnbadmin")
        if not admin:
            User.objects.create_superuser(
                "mybnbadmin", "myeonghan12@gmail.com", "imh04200"
            )
            self.stdout.write(self.style.SUCCESS(f"Superuser created!"))
        else:
            self.stdout.write(self.style.SUCCESS(f"Superuser Exists"))

        # times = options.get("times")
        # for t in range(0, int(times)):
        #     self.stdout.write(self.style.NOTICE("heyhey!\n"))
