from django.core.management.base import BaseCommand
from django_seed import Seed
from users.models import User

# = from rooms import models as room_models


class Command(BaseCommand):
    help = "This command creates many users."

    # This adds '*args'(positional arguments, command line argument). In this case, "--number".
    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            default=2,
            type=int,
            help="How many users do you want to create?",
        )

    def handle(self, *args, **options):
        number = options.get(
            "number", 1
        )  # The number typed after '--number'. The number is default=2 according to the above method.
        seeder = Seed.seeder()
        seeder.add_entity(User, number, {"is_staff": False, "is_superuser": False})
        seeder.execute()

        self.stdout.write(self.style.SUCCESS(f"{number} users created!"))

        # times = options.get("times")
        # for t in range(0, int(times)):
        #     self.stdout.write(self.style.NOTICE("heyhey!\n"))
