from datetime import datetime, timedelta, timezone

from django.conf import settings
from django.test import TestCase, Client
from django.contrib.auth import get_user_model

User = get_user_model()
i18n = settings.I18N


class UserViewTestClass(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_normal_one = User.objects.create_user(username="normal_one", password="123")
        cls.user_normal_two = User.objects.create_user(username="normal_two", password="123")
        cls.user_inactive = User.objects.create_user(username="inactive", password="123", is_active=0)

    def setUp(self) -> None:
        self.c = Client()

    def test_login_normal(self):
        response = self.c.post('/auth/login', {"username": "normal_one", "password": "123"})
        self.assertEqual(response.status_code, 200)

    def test_login_inactive(self):
        response = self.c.post('/auth/login', {"username": "inactive", "password": "123"})
        self.assertEqual(response.status_code, 401)

    def test_retrieve_no_token(self):
        response = self.c.get('/auth/user/1/my')
        self.assertEqual(response.status_code, 401)

    def test_retrieve_yes_token(self):
        login_response = self.c.post('/auth/login', {"username": "normal_one", "password": "123"})
        headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + login_response.json()['access']
        }
        response = self.c.get('/auth/user/1/my', **headers)
        self.assertEqual(response.status_code, 200)

    def test_retrieve_yes_token_get_other_person(self):
        login_response = self.c.post('/auth/login', {"username": "normal_one", "password": "123"})
        headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + login_response.json()['access']
        }
        response = self.c.get('/auth/user/2/my', **headers)
        self.assertEqual(response.status_code, 403)
