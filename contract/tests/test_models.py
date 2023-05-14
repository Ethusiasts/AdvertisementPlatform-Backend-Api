from django.test import TestCase
from contract.models import Contract


class ModelTest(TestCase):
    def test_contract_model(self):
        contract = Contract.objects.create(
            user_id='2',
            advertisement_id='Addis Ababa',
            description='media/plot.PNG',
        )
        self.assertEqual(str(contract), contract.location)
