from django.db import models


class TimeStampedModel(models.Model):

    """ Time Stamped Model """

    created = models.DateTimeField(
        auto_now_add=True
    )  # when a model is created, the created time will be recorded automatically
    updated = models.DateTimeField(
        auto_now=True
    )  # when a model is updated, the time will be recorded automatically

    class Meta:
        abstract = True
