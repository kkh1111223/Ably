import re
from random import randint

from rest_framework.request import Request

from ably_auth.serializers import phone_auth_serializer


def check_create_request_data(request: type(Request)) -> (bool, str):
    return True, ""


def create_phone_auth(request: type(Request),
                      serializer: type(phone_auth_serializer.PhoneAuthSerializer)) -> dict:
    code = str(randint(0, 999999)).zfill(6)

    return {}
