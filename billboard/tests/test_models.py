from django.test import TestCase
from billboard.models import Billboard
from media_agency.models import MediaAgency
from user.models import User


class ModelTest(TestCase):
    def test_billboard_model(self):
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
        billboard = Billboard.objects.create(
            rate='2',
            location='Addis Ababa',
            image='media/plot.PNG',
            width=12,
            height=12,
            media_agency_id=media_agency,
        )
        self.assertEqual(str(billboard), billboard.location)
