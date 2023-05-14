from django.test import TestCase
from agency.models import Agency
from user.models import User


class ModelTest(TestCase):
    def test_agency_model(self):
        user = User.objects.create(
            email="se.biruk.ayalew@gmail.com",
            password='password',
            first_name='Biruk',
            last_name='Ayalew',
            role='user',
            is_verified=False,
            is_staff=False,
        )

        agency = Agency.objects.create(
            user_id=user.id,
            peak_hour=2.2,
            normal=3.1,
            production=3.1,
            with_out_production=3.1,

        )
        self.assertEqual(str(agency), agency.user_id)
