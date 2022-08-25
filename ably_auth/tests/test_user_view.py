from datetime import datetime, timedelta, timezone

from django.conf import settings
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.contrib.sessions.models import Session

User = get_user_model()
i18n = settings.I18N


class UserViewTestClass(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_normal_one = User.objects.create_user(username="normal_one", password="123", mobile_phone="01000000001",
                                                       email="normal_one@google.com", nickname="홀홀넛",
                                                       first_name="코코1", last_name="모")
        cls.user_normal_two = User.objects.create_user(username="normal_two", password="123", mobile_phone="01000000002",
                                                       email="normal_two@naver.com", nickname="관조적시선",
                                                       first_name="난나", last_name="이")
        cls.user_inactive = User.objects.create_user(username="inactive", password="123", mobile_phone="01000000003",
                                                     email="inactive@naver.com", nickname="예민하지않기",
                                                     first_name="코코1", last_name="모", is_active=0)

    def setUp(self) -> None:
        self.c = Client()
        self.valid_session = Session.objects.create(session_key="valid_session",
                                                    expire_date=datetime.now(tz=timezone.utc) + timedelta(days=3))
        self.invalid_session = Session.objects.create(session_key="invalid_session",
                                                      expire_date=datetime.now(tz=timezone.utc) - timedelta(days=3))

    def test_login_normal(self):
        response = self.c.post('/auth/login', {"username": "normal_one", "password": "123"})
        self.assertEqual(response.status_code, 200)

    def test_login_inactive(self):
        response = self.c.post('/auth/login', {"username": "inactive", "password": "123"})
        self.assertEqual(response.status_code, 401)

    def test_my_info_no_token(self):
        response = self.c.get('/auth/user/1/my')
        self.assertEqual(response.status_code, 401)

    def test_my_info_yes_token(self):
        login_response = self.c.post('/auth/login', {"username": "normal_one", "password": "123"})
        headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + login_response.json()['access']
        }
        response = self.c.get('/auth/user/1/my', **headers)
        self.assertEqual(response.status_code, 200)

    def test_my_info_yes_token_get_other_person(self):
        login_response = self.c.post('/auth/login', {"username": "normal_one", "password": "123"})
        headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + login_response.json()['access']
        }
        response = self.c.get('/auth/user/2/my', **headers)
        self.assertEqual(response.status_code, 403)

    def test_create_no_session_key(self):
        response = self.c.post('/auth/user', {"username": "create_test1", "password": "123", "nickname": "얍얍넛",
                                              "mobile_phone": "01000000004", "email": "create_test@google.com",
                                              "first_name": "이", "last_name": "웨"})
        self.assertEqual(response.status_code, 403)

    def test_create_omit_mandatory_data(self):
        response = self.c.post('/auth/user', {"username": "create_test2", "password": "123", "nickname": "누워요",
                                              "mobile_phone": "01000000005", "first_name": "디", "last_name": "샨",
                                              "session_key": "valid_session"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['msg'], i18n['resp_msg']['no_mandatory_data'])

    def test_create_restricted_data(self):
        response = self.c.post('/auth/user', {"username": "create_test3", "email": "create_test3@google.com",
                                              "password": "123", "nickname": "니니녜녜", "mobile_phone": "01000000006",
                                              "session_key": "valid_session", "first_name": "제나", "last_name": "아",
                                              "is_superuser": True})
        self.assertEqual(response.status_code, 400)

    def test_create_success(self):
        response = self.c.post('/auth/user', {"username": "create_test4", "password": "123", "nickname": "녜녜니니",
                                              "mobile_phone": "01000000007", "email": "createtest4@google.com",
                                              "session_key": "valid_session", "first_name": "제나", "last_name": "아"})
        self.assertEqual(response.status_code, 201)

    def test_reset_password_no_session_key(self):
        response = self.c.post('/auth/user/reset_password',
                               {"username": "normal_two", "password": "12344",  "mobile_phone": "01000000002"})
        self.assertEqual(response.status_code, 403)

    def test_reset_password_omit_mandatory_data(self):
        response = self.c.post('/auth/user/reset_password',
                               {"username": "normal_two", "session_key": "valid_session", "mobile_phone": "01000000002"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['msg'], i18n['resp_msg']['no_mandatory_data'])

    def test_reset_password_user_phone_not_match(self):
        response = self.c.post('/auth/user/reset_password',
                               {"username": "normal_two", "session_key": "valid_session",
                                "mobile_phone": "01012341234", "password": "112233"})
        self.assertEqual(response.status_code, 400)

    def test_reset_password_success(self):
        response = self.c.post('/auth/user/reset_password',
                               {"username": "normal_two", "session_key": "valid_session",
                                "mobile_phone": "01000000002", "password": "112233"})
        self.assertEqual(response.status_code, 200)

        login_response = self.c.post('/auth/login', {"username": "normal_two", "password": "112233"})
        self.assertEqual(login_response.status_code, 200)
