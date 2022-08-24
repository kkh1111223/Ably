import jwt

from rest_framework.request import Request

from django.contrib.auth import settings, get_user_model

SECRET_KEY = settings.SECRET_KEY
i18n = settings.I18N
User = get_user_model()


def compare_user_id(token: str, user_id: str) -> bool:
    jwt_data = jwt.decode(str(token), SECRET_KEY, ["HS256"])
    if int(jwt_data.get('user_id', 0)) != int(user_id):
        return False
    return True


def check_create_request_data(request: Request) -> (bool, str):
    mandatory_data = ['username', 'password', 'nickname', 'email', 'mobile_phone', 'first_name', 'last_name']
    restricted_data = ['is_staff', 'is_superuser']
    if [i for i in mandatory_data if i not in request.data.keys()] \
            or [i for i in restricted_data if i in request.data.keys()]:
        return False, i18n['resp_msg']['no_mandatory_data']

    return True, ""


def check_reset_password_request_data(request: Request) -> (bool, str):
    mandatory_data = ['username', 'password', 'mobile_phone']
    if [i for i in mandatory_data if i not in request.data.keys()]:
        return False, i18n['resp_msg']['no_mandatory_data']

    try:
        User.objects.get(username=request.data['username'], mobile_phone=request.data['mobile_phone'])
    except User.DoesNotExist:
        return False, i18n['resp_msg']['no_such_user']

    return True, ""
