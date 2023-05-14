from unittest import mock
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from media_agency.models import MediaAgency

from user.models import User


class BaseTest(TestCase):

    def setUp(self):
        self.media_agency_url = reverse('media-agencies')
        self.user = {
            "email": "test@gmail.com",
            "password": "12345678",
            "first_name": "test",
            "last_name": "test",
            "role": "customer",
        }
        user = User.objects.create(**self.user)

        self.media_agency = {
            'user': user.id,
            'company_name': 'sheger',
            'tin_number': 12,
            'is_verified': True,
        }

        self.media_agency2 = {
            'user': user,
            'company_name': 'sheger',
            'tin_number': 12,
            'is_verified': True,
        }

        # media_agency = MediaAgency.objects.create(**self.media_agency2)

        # self.url = reverse('media_agency', args=[media_agency.id])

        return super().setUp()


class MediaAgencyTest(BaseTest):
    def test_can_create_new_media_agency(self):
        response = self.client.post(self.media_agency_url, self.media_agency)
        self.assertEqual(response.status_code, 201)

    def test_can_get_all_media_agencies(self):
        response = self.client.get(self.media_agency_url)
        self.assertEqual(response.status_code, 200)

    # def test_can_get_media_agency(self):
    #     media_agency = MediaAgency.objects.create(**self.media_agency2)
    #     response = self.client.get(
    #         reverse('media_agency', kwargs={'id': media_agency.id}))
    #     self.assertEqual(response.status_code, 200)

    def test_can_delete_media_agency(self):
        media_agency = MediaAgency.objects.create(**self.media_agency2)
        response = self.client.delete(
            reverse('media-agency', kwargs={'id': media_agency.id}))
        self.assertEqual(response.status_code, 204)

    # def test_can_update_media_agency(self):
    #     response = self.client.put(
    #         self.url, self.media_agency2)
    #     self.assertEqual(response.status_code, 200)
