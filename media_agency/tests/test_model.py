from django.test import TestCase
from media_agency.models import MediaAgency
from user.models import User


class ModelTest(TestCase):
    def test_media_agency_model(self):
        user = User.objects.create(
            email="se.biruk.ayalew@gmail.com",
            password='password',
            first_name='Biruk',
            last_name='Ayalew',
            role='user',
            is_verified=False,
            is_staff=False,
        )
        media_agency = MediaAgency.objects.create(
            user=user,
            company_name='sheger',
            tin_number=12,
            is_verified=True,
        )
        self.assertEqual(str(media_agency), media_agency.company_name)
