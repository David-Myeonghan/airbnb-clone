# from os # first from Python
from django.db import models  # second from Django
from django_countries.fields import CountryField  # third from Third-party app
from core import models as core_models  # fourth from my app.

# Created to make room type, amenities, facilities, house rule,... etc. And each item in each class should be easily managed in admin page by non-programmer user.
class AbstractItem(core_models.TimeStampedModel):

    """ Abstract Item """

    name = models.CharField(max_length=80)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class RoomType(AbstractItem):  # many to many

    """ RoomType Model Definition """

    class Meta:
        verbose_name_plural = "Room Type"


class Amenity(AbstractItem):
    """ Amenity Model Definition """

    class Meta:
        verbose_name_plural = "Amenities"


class Facility(AbstractItem):
    """ Facility Model Deficition"""

    class Meta:
        verbose_name_plural = "Facilities"


class HouseRule(AbstractItem):
    """ HouseRule Model Deficition"""

    class Meta:
        verbose_name_plural = "House Rules"


# Photo links to -> Room links to-> User
class Photo(core_models.TimeStampedModel):
    """ Photo Model Definition """

    caption = models.CharField(max_length=80)
    file = models.ImageField(upload_to="room_photos")
    # Uploads phots in 'room_photos' folder in 'uploads' folder
    room = models.ForeignKey(
        "Room", related_name="photos", on_delete=models.CASCADE
    )  # Python reads text from top to bottom

    def __str__(self):
        return self.caption


class Room(core_models.TimeStampedModel):

    """ Room Model Definition """

    name = models.CharField(max_length=140)
    description = models.TextField()
    country = CountryField()
    city = models.CharField(max_length=80)
    price = models.IntegerField()
    address = models.CharField(max_length=140)
    guests = models.IntegerField()
    beds = models.IntegerField()
    bedrooms = models.IntegerField()
    baths = models.IntegerField()
    check_in = models.TimeField()
    check_out = models.TimeField()
    instant_book = models.BooleanField(default=False)
    host = models.ForeignKey(
        "users.User", related_name="rooms", on_delete=models.CASCADE
    )  # many rooms - to one user # CASCADE: WATERFALL. if we delete user, rooms will be deleted together.
    room_type = models.ForeignKey(
        "RoomType", related_name="rooms", on_delete=models.SET_NULL, null=True
    )
    amenities = models.ManyToManyField(
        "Amenity", related_name="rooms", blank=True
    )  # related_name = "rooms" -> room type has "rooms"
    facilities = models.ManyToManyField("Facility", related_name="rooms", blank=True)
    house_rules = models.ManyToManyField("HouseRule", related_name="rooms", blank=True)
    # photo is needed...

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.city = str.capitalize(self.city)
        super().save(*args, **kwargs)  # Call the real save() method

    # Calculates the whole average reviews users wrote.
    def total_rating(self):
        all_reviews = self.reviews.all()
        all_ratings = 0
        if len(all_reviews) > 0:
            for review in all_reviews:
                # print(review.accuracy)
                all_ratings += review.rating_average()
            return all_ratings / len(all_reviews)
            # = return all_ratings / self.reviews.count()
        return 0
