import re
from random import randint
from typing import Type, TypeVar

from rest_framework.request import Request

from ably_auth.serializers import phone_auth_serializer
from ably_auth.models import phone_auth_model

PhoneAuthType = TypeVar('PhoneAuthType', bound=phone_auth_model.PhoneAuth)


def regularize_phone_number(phone_number: str) -> str:
    return re.sub('[^\d]', '', phone_number)


def check_create_request_data(request: Request) -> (bool, str):
    mandatory_data = ['phone_number']
    if [i for i in mandatory_data if i not in request.data.keys()]:
        return False, "필수 정보들이 누락되었습니다."

    phone_number = regularize_phone_number(request.data['phone_number'])
    if not re.match('^01([0|1|6|7|8|9])-?([0-9]{3,4})-?([0-9]{4})$', phone_number):
        return False, "잘못 된 핸드폰번호가 입력되었습니다."

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
        return False, "필수 정보들이 누락되었습니다."

    return True, ""


def verify_phone_authentication(request: Request, phone_auth_instance: Type[PhoneAuthType]) -> (bool, str):
    verification_code = request.data['verification_code']
    if phone_auth_instance.trial == 0:
        return False, "만료 된 인증입니다. 인증을 재발급 받아주세요."

    if verification_code == phone_auth_instance.verification_code:
        return True, ""
    else:
        phone_auth_instance.trial = phone_auth_instance.trial - 1
        phone_auth_instance.save()
        return False, "인증 실패. 인증번호를 다시 확인해주세요."
