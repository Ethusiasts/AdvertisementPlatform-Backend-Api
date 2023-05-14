from unittest import mock
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from proposal.models import Proposal
from proposal.models import Proposal
from django.core.files.base import File

from user.models import User


class BaseTest(TestCase):
    def setUp(self):
        self.proposal_url = reverse('proposals')

        self.user = {
            "email": "test@gmail.com",
            "password": "12345678",
            "first_name": "test",
            "last_name": "test",
            "role": "customer",
        }
        user = User.objects.create(**self.user)

        self.proposal = {}
        proposal = Proposal.objects.create(**self.user)

        self.proposal = {
            'user_id': user.id,
            'proposal_id': proposal.id,
            'description': 'test description',
        }

        return super().setUp()


# class ProposalTest(BaseTest):
    # def test_can_create_new_proposal(self):
    #     response = self.client.post(self.proposal_url, self.proposal)
    #     self.assertEqual(response.status_code, 400)

    # def test_can_get_all_proposals(self):
    #     response = self.client.get(self.proposal_url)
    #     self.assertEqual(response.status_code, 400)

    # def test_can_delete_billboard(self):
    #     billboard = Billboard.objects.create(**self.billboard2)
    #     response = self.client.delete(
    #         reverse('billboard', kwargs={'id': billboard.id}))
    #     self.assertEqual(response.status_code, 204)

    # def test_can_get_proposal(self):
    #     proposal = Proposal.objects.create(**self.proposal2)
    #     response = self.client.get(
    #         reverse('proposal', kwargs={'id': proposal.id}))
    #     self.assertEqual(response.status_code, 200)
