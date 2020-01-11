from django.contrib import admin
from django.utils.html import mark_safe
from . import models


@admin.register(models.RoomType, models.Facility, models.Amenity, models.HouseRule)
class ItemAdmin(admin.ModelAdmin):

    """ Item Admin Definition """

    list_display = ("name", "used_by")

    def used_by(self, obj):
        return obj.rooms.count()
        # = return obj.room_set.count()


class PhotoInline(admin.TabularInline):

    model = models.Photo


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):

    """ Room Admin Definition """

    inlines = (PhotoInline,)

    fieldsets = (
        (
            "Basic Info",
            {"fields": ("name", "description", "country", "city", "address", "price")},
        ),
        ("Times", {"fields": ("check_in", "check_out", "instant_book")},),
        ("Spaces", {"fields": ("guests", "beds", "bedrooms", "baths",)}),
        (
            "More About the Space",
            {
                "classes": ("collapse",),
                "fields": ("amenities", "facilities", "house_rules",),
            },
        ),
        ("Last Details", {"fields": ("host",)}),
    )

    list_display = (
        "name",
        "country",
        "city",
        "price",
        "guests",
        "beds",
        "bedrooms",
        "baths",
        "check_in",
        "check_out",
        "instant_book",
        "count_amenities",
        "count_photos",
        "total_rating",
    )

    ordering = ("name", "price", "bedrooms")

    list_filter = (
        "instant_book",
        "host__superhost",
        "city",
        "room_type",
        "amenities",
        "facilities",
        "house_rules",
        "country",
    )

    raw_id_fields = ("host",)
    # gives opportunity to see your foreign key in a better way.
    # If there are so many users to choose or search, this way would be better.

    search_fields = (
        "=city",
        "^host__username",
    )
    filter_horizontal = (
        "amenities",
        "facilities",
        "house_rules",
    )

    def count_amenities(self, obj):
        # cannot click to order in admin panel, because Django knows this is a function, which is non-orderable
        # print(obj.amenities.all()) #shows all amenities in this room
        return obj.amenities.count()

    # count_amenities.short_description = "Django Super Customisable"

    def count_photos(self, obj):
        return obj.photos.count()
        # = return obj.photo_set.count()


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):

    """ Photo Admin Definition """

    list_display = ("__str__", "get_thumbnail")

    def get_thumbnail(self, obj):
        # image file is not just a paht. it's one class.
        return mark_safe(f'<img width="50px" src="{obj.file.url}" />')

    get_thumbnail.short_description = "Thumbnail"

