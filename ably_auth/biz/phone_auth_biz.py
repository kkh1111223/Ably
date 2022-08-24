import re
from datetime import datetime, timedelta, timezone
from random import randint
from typing import Type, TypeVar

from rest_framework.request import Request

from django.conf import settings

from ably_auth.serializers import phone_auth_serializer
from ably_auth.models import phone_auth_model

PhoneAuthType = TypeVar('PhoneAuthType', bound=phone_auth_model.PhoneAuth)
i18n = settings.I18N


def regularize_phone_number(phone_number: str) -> str:
    return re.sub('[^\d]', '', phone_number)


def check_create_request_data(request: Request) -> (bool, str):
    mandatory_data = ['phone_number']
    if [i for i in mandatory_data if i not in request.data.keys()]:
        return False, i18n['resp_msg']['no_mandatory_data']

    phone_number = regularize_phone_number(request.data['phone_number'])
    if not re.match('^01([0|1|6|7|8|9])-?([0-9]{3,4})-?([0-9]{4})$', phone_number):
        return False, i18n['resp_msg']['wrong_phone_number']

    return True, ""


def create_phone_authentication(request: Request,
                                serializer: phone_auth_serializer.PhoneAuthSerializer) -> dict:
    verification_code = str(randint(0, 999999)).zfill(6)
    data = {
        "phone_number": regularize_phone_number(request.data['phone_number']),
        "verification_code": verification_code,
    }
    serializer.initial_data = data
    if serializer.is_valid():
        serializer.save()
    return serializer.data


def check_verify_request_data(request: Request) -> (bool, str):
    mandatory_data = ['verification_code']
    if [i for i in mandatory_data if i not in request.data.keys()]:
        return False, i18n['resp_msg']['no_mandatory_data']
    return True, ""


def verify_phone_authentication(request: Request, phone_auth_instance: Type[PhoneAuthType]) -> (bool, str):
    verification_code = request.data['verification_code']
    is_expired = phone_auth_instance.created_time < (datetime.now(tz=timezone.utc) - timedelta(minutes=3))
    if phone_auth_instance.trial == 0 or phone_auth_instance.revoked is True or is_expired:
        return False, i18n['resp_msg']['invalid_verification']

    if verification_code == phone_auth_instance.verification_code:
        request.session.save(must_create=True)
        phone_auth_instance.revoked = True
        phone_auth_instance.save()
        return True, ""
    else:
        left_trial = phone_auth_instance.trial - 1
        phone_auth_instance.trial = left_trial
        phone_auth_instance.revoked = True if left_trial == 0 else False
        phone_auth_instance.save()
        return False, i18n['resp_msg']['wrong_verification_code']
