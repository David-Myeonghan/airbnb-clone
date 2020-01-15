import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from lists import models as list_models
from users import models as user_models
from rooms import models as room_models

NAME = "lists"


class Command(BaseCommand):
    help = f"This command creates many {NAME}."

    # This adds '*args'(positional arguments, command line argument). In this case, "--number".
    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            default=2,
            type=int,
            help=f"How many {NAME} do you want to create?",
        )

    def handle(self, *args, **options):
        number = options.get(
            "number", 1
        )  # The number typed after '--number'. The number is default=2 according to the above method.
        seeder = Seed.seeder()
        users = user_models.User.objects.all()
        rooms = room_models.Room.objects.all()
        seeder.add_entity(
            list_models.List, number, {"user": lambda x: random.choice(users),},
        )
        created = seeder.execute()
        cleaned = flatten(list(created.values()))
        for pk in cleaned:
            one_list = list_models.List.objects.get(pk=pk)
            # rooms[2:5] : get rooms from the list #2 to 5.
            to_add = rooms[random.randint(0, 5) : random.randint(6, 30)]
            one_list.rooms.add(*to_add)  # to add many-to-many field: add()
            # *to_add gets the actual rooms not query set

        self.stdout.write(self.style.SUCCESS(f"{number} {NAME} created!"))

        # times = options.get("times")
        # for t in range(0, int(times)):
        #     self.stdout.write(self.style.NOTICE("heyhey!\n"))
