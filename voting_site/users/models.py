from django.contrib.auth.models import AbstractUser
from django.db import models

from enum import Enum


class Gender(Enum):
    Male = 'male'
    Female = 'female'

    @classmethod
    def get_choices(cls):
        return [(el.value, name) for name, el in cls.__members__.items()]


class User(AbstractUser):
    incorrect_attempts = models.PositiveSmallIntegerField(default=0)
    age = models.PositiveSmallIntegerField(default=0)
    gender = models.CharField(
        max_length=10,
        choices=Gender.get_choices()
    )
