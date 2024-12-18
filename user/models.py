from django.db import models
from django.contrib.auth.models import AbstractUser
from main.models import Point


class User(AbstractUser):
	points = models.ManyToManyField(Point)
