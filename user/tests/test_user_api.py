from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from user.models import user_reset_password_token
from django.urls import reverse
from user.models import User
from user.serializers import UserGetSerializer
from rest_framework.authtoken.models import Token


class BaseTest(TestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.forgot_password_url = reverse('forgot-password')

        self.user = {
            "email": "test@gmail.com",
            "password": "12345678",
            "first_name": "test",
            "last_name": "test",
            "role": "customer",
        }
        self.user_invalid_role = {
            "email": "test@gmail.com",
            "password": "12345678",
            "first_name": "test",
            "last_name": "test",
            "role": "Manager"
        }
        self.user_credential_with_invalid_email = {
            "email": "unknown@gmail.com",
            "password": "12345678",
        }
        self.user_credential_with_valid_email_and_password = {
            "email": "test@gmail.com",
            "password": "12345678",
        }
        self.user_credential_account_not_activated = {
            "email": "test@gmail.com",
            "password": "12345678",
        }
        self.user_with_invalid_email = {
            "email": "unknown@gmail.com",
        }

        return super().setUp()


class RegisterTest(BaseTest):
    def test_can_register_user_with_invalid_role(self):
        response = self.client.post(self.register_url, self.user_invalid_role)
        self.assertEqual(response.status_code, 400)

    def test_can_register_user_with_taken_email(self):
        self.client.post(self.register_url, self.user)
        response = self.client.post(self.register_url, self.user)
        self.assertEqual(response.status_code, 400)

    def test_can_send_account_activation_email(self):
        response = self.client.post(self.register_url, self.user)
        self.assertEqual(response.status_code, 200)


class LoginTest(BaseTest):
    def test_can_login_with_invalid_emailorpasswrord(self):
        self.client.post(self.register_url, self.user)
        response = self.client.post(
            self.login_url, self.user_credential_with_invalid_email)
        self.assertEqual(response.status_code, 400)

    def test_can_login_with_account_not_activated(self):
        self.client.post(self.register_url, self.user)
        response = self.client.post(
            self.login_url, self.user_credential_account_not_activated)
        self.assertEqual(response.status_code, 400)

    def test_can_login_sucessfully(self):
        user = User.objects.create_user(**self.user)
        token = user_reset_password_token._create_token(user)
        response = self.client.get(
            reverse('activate', kwargs={'token': token}))
        response = self.client.post(
            self.login_url, self.user_credential_with_valid_email_and_password)
        self.assertEqual(response.status_code, 200)


class AccountActivationTest(BaseTest):
    def test_can_activate_account(self):
        user = User.objects.create_user(**self.user)
        token = user_reset_password_token._create_token(user)
        response = self.client.get(
            reverse('activate', kwargs={'token': token}))
        self.assertEqual(response.status_code, 200)

    def test_cannot_activate_account(self):
        token = '6a8568eefd48570dcea20cdd014aed2e0ec4b193'
        response = self.client.get(
            reverse('activate', kwargs={'token': token}))
        self.assertEqual(response.status_code, 400)


class ForgotPassword(BaseTest):
    def test_can_forgot_password_with_invalid_email(self):
        self.client.post(self.register_url, self.user)
        response = self.client.post(
            self.forgot_password_url, self.user_with_invalid_email)
        self.assertEqual(response.status_code, 404)

    def test_can_forgot_pasword_sucessfully(self):
        self.client.post(self.register_url, self.user)
        response = self.client.post(self.forgot_password_url, self.user)
        self.assertEqual(response.status_code, 200)
