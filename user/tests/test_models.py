from django.test import TestCase
from user import models


class ModelTest(TestCase):
    def test_user_model(self):
        user = models.User.objects.create(
            email="se.biruk.ayalew@gmail.com",
            password='password',
            first_name='Biruk',
            last_name='Ayalew',
            role='user',
            is_verified=False,
            is_staff=False,
        )
        self.assertEqual(str(user), user.email)
