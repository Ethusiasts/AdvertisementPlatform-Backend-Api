from django.test import TestCase
from billboard.models import Billboard


class ModelTest(TestCase):
    def test_billboard_model(self):
        billboard = Billboard.objects.create(
            rate='2',
            location='Addis Ababa',
            image='media/plot.PNG',
            width=12,
            height=12,
            landowner_id=1,
        )
        self.assertEqual(str(billboard), billboard.location)
