from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    nickname = models.CharField(max_length=20)
    mobile_phone = models.CharField(max_length=11, null=True)
