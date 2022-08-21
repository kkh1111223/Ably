import re
from random import randint

from rest_framework.request import Request

from ably_auth.serializers import phone_auth_serializer


def check_create_request_data(request: type(Request)) -> (bool, str):
    mandatory_data = ['phone_number']
    if [i for i in mandatory_data if i not in request.data.keys()]:
        return False, "필수 정보들이 누락되었습니다."

    phone_number = re.sub('[^\d]', '', request.data['phone_number'])
    if not re.match('^01([0|1|6|7|8|9])-?([0-9]{3,4})-?([0-9]{4})$', phone_number):
        return False, "잘못 된 핸드폰번호가 입력되었습니다."

    return True, ""


def create_phone_auth(request: type(Request),
                      serializer: type(phone_auth_serializer.PhoneAuthSerializer)) -> dict:
    code = str(randint(0, 999999)).zfill(6)
    
    return {}
