import jwt

from django.contrib.auth import settings

SECRET_KEY = settings.SECRET_KEY


def compare_user_id(token: str, user_id: str) -> bool:
    jwt_data = jwt.decode(str(token), SECRET_KEY, ["HS256"])
    if int(jwt_data.get('user_id', 0)) != int(user_id):
        return False
    return True
