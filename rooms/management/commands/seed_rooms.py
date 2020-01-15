import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from rooms import models as room_models

# = from rooms import models as room_models
from users import models as user_models


class Command(BaseCommand):
    help = "This command creates many rooms."

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            default=2,
            type=int,
            help="How many rooms do you want to create?",
        )

    # Room model cannnot be created without foreign key 'host'.
    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()

        # THIS IS NOT GOOD PRACTICE!! NEVER EVER USE THIS COMMAND IF THERE ARE PLENTY OF USERS IN DB.
        all_users = user_models.User.objects.all()  # All users from DB
        room_types = room_models.RoomType.objects.all()
        # print(room_types, all_users)
        seeder.add_entity(
            room_models.Room,
            number,
            {
                "name": lambda x: seeder.faker.address(),
                "host": lambda x: random.choice(all_users),
                "room_type": lambda x: random.choice(room_types),
                "price": lambda x: random.randint(1, 300),
                "guests": lambda x: random.randint(1, 5),
                "beds": lambda x: random.randint(1, 5),
                "bedrooms": lambda x: random.randint(1, 5),
                "baths": lambda x: random.randint(1, 5),
            },
        )  # 'x' is a room.
        created_photos = seeder.execute()
        created_clean = flatten(
            list(created_photos.values())
        )  # extract the flattened list([number]) from nested lists.

        amenities = room_models.Amenity.objects.all()
        facilities = room_models.Facility.objects.all()
        rules = room_models.HouseRule.objects.all()

        for pk in created_clean:
            room = room_models.Room.objects.get(pk=pk)  # a room instance created above
            for i in range(3, random.randint(10, 30)):  # add photos
                room_models.Photo.objects.create(
                    caption=seeder.faker.sentence(),
                    file=f"room_photos/{random.randint(1,31)}.webp",
                    room=room,  # manage foreign key
                )
            for a in amenities:  # add amenities
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:  # if even,
                    # manage many to many # the way add something in many to many field.
                    room.amenities.add(a)
            for f in facilities:  # add facilities
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:  # if even,
                    # manage many to many # the way add something in many to many field.
                    room.facilities.add(f)
            for r in rules:  # add house rules
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:  # if even,
                    # manage many to many # the way add something in many to many field.
                    room.house_rules.add(r)
        self.stdout.write(self.style.SUCCESS(f"{number} rooms created!"))

        # times = options.get("times")
        # for t in range(0, int(times)):
        #     self.stdout.write(self.style.NOTICE("heyhey!\n"))
