from unittest import mock
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from billboard.models import Billboard
from media_agency.models import MediaAgency
from io import BytesIO
from PIL import Image
from django.core.files.base import File

from user.models import User


class BaseTest(TestCase):
    @staticmethod
    def get_image_file(name='test.png', ext='png', size=(50, 50), color=(256, 0, 0)):
        file_obj = BytesIO()
        image = Image.new("RGB", size=size, color=color)
        image.save(file_obj, ext)
        file_obj.seek(0)
        return File(file_obj, name=name)

    def setUp(self):
        self.billboard_url = reverse('billboards')

        self.user = {
            "email": "test@gmail.com",
            "password": "12345678",
            "first_name": "test",
            "last_name": "test",
            "role": "customer",
        }
        user = User.objects.create(**self.user)

        self.media_agency = {
            'user': user,
            'company_name': 'sheger',
            'tin_number': 12,
            'is_verified': True,
        }
        media_agency = MediaAgency.objects.create(**self.media_agency)

        self.billboard1 = {
            'rate': 2,
            'location': 'Addis Ababa',
            'image': self.get_image_file(),
            'width': 12,
            'height': 12,
            'media_agency_id': media_agency.id,
            'approved': True,
            'production': True
        }

        self.billboard2 = {
            'rate': 2,
            'location': 'Bole',
            'image': self.get_image_file(),
            'width': 12,
            'height': 12,
            'media_agency_id': media_agency,
            'approved': True,
            'production': True
        }

        # billboard = Billboard.objects.create(**self.billboard2)

        # self.url = reverse('billboard', args=[billboard.id])

        return super().setUp()


class BillboardTest(BaseTest):
    def test_can_create_new_billboard(self):
        response = self.client.post(self.billboard_url, self.billboard1)
        self.assertEqual(response.status_code, 201)

    def test_can_get_all_billboards(self):
        response = self.client.get(self.billboard_url)
        self.assertEqual(response.status_code, 200)

    # def test_can_get_billboard(self):
    #     billboard = Billboard.objects.create(**self.billboard2)
    #     response = self.client.get(
    #         reverse('billboard', kwargs={'id': billboard.id}))
    #     self.assertEqual(response.status_code, 200)

    def test_can_delete_billboard(self):
        billboard = Billboard.objects.create(**self.billboard2)
        response = self.client.delete(
            reverse('billboard', kwargs={'id': billboard.id}))
        self.assertEqual(response.status_code, 204)

    # def test_can_update_billboard(self):
    #     response = self.client.put(
    #         self.url, self.billboard2)
    #     self.assertEqual(response.status_code, 200)
