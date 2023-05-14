from django.test import TestCase
from proposal.models import Proposal


class ModelTest(TestCase):
    def test_proposal_model(self):
        proposal = Proposal.objects.create(
            user_id='2',
            advertisement_id='Addis Ababa',
            description='media/plot.PNG',
        )
        self.assertEqual(str(proposal), proposal.location)
