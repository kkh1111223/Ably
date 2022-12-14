from datetime import datetime, timedelta, timezone

from django.conf import settings
from django.test import TestCase, Client

from ably_auth.models import phone_auth_model

i18n = settings.I18N


class PhoneAuthViewTestClass(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.phone_auth_fail = phone_auth_model.PhoneAuth.objects.create(phone_number="01012341234",
                                                                        verification_code="123456")
        cls.phone_auth_success = phone_auth_model.PhoneAuth.objects.create(phone_number="01043214321",
                                                                           verification_code="654321")
        cls.phone_auth_revoked = phone_auth_model.PhoneAuth.objects.create(phone_number="01043214321",
                                                                           verification_code="654321",
                                                                           revoked=1)
        cls.phone_auth_expired = phone_auth_model.PhoneAuth.objects.create(phone_number="01043214321",
                                                                           verification_code="654321",
                                                                           created_time=datetime.now(tz=timezone.utc)
                                                                                        - timedelta(minutes=3))

    def setUp(self) -> None:
        self.c = Client()

    def test_create_omit_mandatory_data(self):
        response = self.c.post('/auth/phone_auth', {"foo": "bar"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['msg'], i18n['resp_msg']['no_mandatory_data'])

    def test_create_wrong_phone_number(self):
        response = self.c.post('/auth/phone_auth', {"phone_number": "010123412344"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['msg'], i18n['resp_msg']['wrong_phone_number'])

    def test_create_success(self):
        response = self.c.post('/auth/phone_auth', {"phone_number": "01012341234"})
        self.assertEqual(response.status_code, 201)

    def test_verify_not_existing_data(self):
        response = self.c.post('/auth/phone_auth/99999999/verify', {"verification_code": "123456"})
        self.assertEqual(response.status_code, 404)

    def test_verify_omit_mandatory_data(self):
        response = self.c.post('/auth/phone_auth/1/verify', {"foo": "bar"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['msg'], i18n['resp_msg']['no_mandatory_data'])

    def test_verify_fail_verification(self):
        for i in range(3):
            response = self.c.post('/auth/phone_auth/1/verify', {"verification_code": "000000"})
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.json()['msg'], i18n['resp_msg']['wrong_verification_code'])

    def test_verify_no_trial_verification(self):
        self.phone_auth_fail.trial = 0
        self.phone_auth_fail.save()
        response = self.c.post('/auth/phone_auth/1/verify', {"verification_code": "000000"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['msg'], i18n['resp_msg']['invalid_verification'])

    def test_verify_success(self):
        verification_code = self.phone_auth_success.verification_code
        response = self.c.post('/auth/phone_auth/2/verify', {"verification_code": verification_code})
        self.assertEqual(response.status_code, 200)

    def test_verify_revoked_verification(self):
        verification_code = self.phone_auth_revoked.verification_code
        response = self.c.post('/auth/phone_auth/3/verify', {"verification_code": verification_code})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['msg'], i18n['resp_msg']['invalid_verification'])

    def test_verify_expired_verification(self):
        verification_code = self.phone_auth_expired.verification_code
        response = self.c.post('/auth/phone_auth/3/verify', {"verification_code": verification_code})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['msg'], i18n['resp_msg']['invalid_verification'])