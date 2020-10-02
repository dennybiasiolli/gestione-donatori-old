from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient

from donatori.models import Sezione


class MockedTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.avis1 = User.objects.create_user(
            'avis1', 'avis1@email.it', 'avis1')
        self.avis2 = User.objects.create_user(
            'avis2', 'avis2@email.it', 'avis2')

        self.sezione1 = Sezione.objects.create(
            utente=self.avis2,
            descrizione='AVIS 2',
            ragione_sociale='AVIS ABC',
            indirizzo='Via Roma 12',
        )

    def authenticate(self, username, password):
        response = self.client.post('/api/token/', {
            'username': username,
            'password': password,
        })
        self.access_token = response.data['access']
        self.refresh_token = response.data['refresh']
