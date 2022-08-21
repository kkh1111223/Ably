import re
from random import randint

from rest_framework.request import Request

from ably_auth.serializers import phone_auth_serializer


def regularize_phone_number(phone_number: str) -> str:
    return re.sub('[^\d]', '', phone_number)


def check_create_request_data(request: type(Request)) -> (bool, str):
    mandatory_data = ['phone_number']
    if [i for i in mandatory_data if i not in request.data.keys()]:
        return False, "필수 정보들이 누락되었습니다."

    phone_number = regularize_phone_number(request.data['phone_number'])
    if not re.match('^01([0|1|6|7|8|9])-?([0-9]{3,4})-?([0-9]{4})$', phone_number):
        return False, "잘못 된 핸드폰번호가 입력되었습니다."

    return True, ""


def create_phone_authentication(request: type(Request),
                                serializer: type(phone_auth_serializer.PhoneAuthSerializer)) -> dict:
    verification_code = str(randint(0, 999999)).zfill(6)
    data = {
        "phone_number": regularize_phone_number(request.data['phone_number']),
        "verification_code": verification_code,
    }
    serializer.initial_data = data
    if serializer.is_valid():
        serializer.save()
    return serializer.data
