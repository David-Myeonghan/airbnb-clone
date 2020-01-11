from django.contrib.auth.models import AbstractUser
from django.db import models

# This will be translated into SQL language
class User(AbstractUser):  # Inheritance: copy and paste AbstractUser into User class.

    """ Custom User Model """

    GENDER_MALE = "male"
    GENDER_FEMALE = "female"
    GENDER_OTHER = "other"

    GENDER_CHOICES = (
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE, "Female"),
        (GENDER_OTHER, "Other"),
    )

    LANGUAGE_KOREAN = "kr"
    LANGUAGE_ENGLISH = "en"

    LANGUAGE_CHOICES = (
        (LANGUAGE_KOREAN, "Korean"),
        # THIS GO TO DB // THIS SHOWN ON THE FORM
        (LANGUAGE_ENGLISH, "English"),
    )

    CURRENCY_USD = "usd"
    CURRENCY_KRW = "krw"

    CURRENCY_CHOICES = ((CURRENCY_USD, "USD"), (CURRENCY_KRW, "KRW"))

    avatar = models.ImageField(upload_to="avatars", blank=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=10, blank=True)
    bio = models.TextField(blank=True)
    birthdate = models.DateField(blank=True, null=True)
    language = models.CharField(choices=LANGUAGE_CHOICES, max_length=2, blank=True)
    currency = models.CharField(choices=CURRENCY_CHOICES, max_length=3, blank=True)
    superhost = models.BooleanField(default=False)

    # def __str__(self):
    #     return self.username
