from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class PhoneAuth(models.Model):
    objects = models.Manager()
    id = models.AutoField(primary_key=True)
    created_time = models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField(max_length=11)
    verification_code = models.CharField(max_length=6)
    trial = models.IntegerField(default=3)
    revoked = models.BooleanField(default=False)

    class Meta:
        db_table = "phone_auth"
