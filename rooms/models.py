# from os # first from Python
from django.utils import timezone
from django.db import models  # second from Django
from django.urls import reverse
from django_countries.fields import CountryField  # third from Third-party app
from core import models as core_models  # fourth from my app.
from cal import Calendar

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

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.city = str.capitalize(self.city)
        super().save(*args, **kwargs)  # Call the real save() method

    def get_absolute_url(self):  # in admin panel, go to the returned url, and get pk
        return reverse(
            "rooms:detail", kwargs={"pk": self.pk}
        )  # 'rooms' namespace from urls.py in config

    # Calculates the whole average reviews of one room users wrote.
    def total_rating(self):
        all_reviews = self.reviews.all()
        all_ratings = 0
        if len(all_reviews) > 0:
            for review in all_reviews:
                # print(review.accuracy)
                all_ratings += review.rating_average()
            return round((all_ratings / len(all_reviews)), 2)
            # = return all_ratings / self.reviews.count()
        return 0

    def first_photo(self):
        try:
            # load query set. and put the content of queryset using unpacking values(,)
            (photo,) = self.photos.all()[:1]
            return photo.file.url  # not query set anymore.
        except ValueError:
            return None

    def get_next_four_photos(self):
        photos = self.photos.all()[1:5]
        return photos

    def get_calendars(self):
        now = timezone.now()
        this_year = now.year
        this_month = now.month
        next_month = this_month + 1
        if this_month == 12:
            next_month = 1
        this_month_cal = Calendar(this_year, this_month)
        next_month_cal = Calendar(this_year, next_month)
        return [this_month_cal, next_month_cal]
