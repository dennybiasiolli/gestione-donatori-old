from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient, force_authenticate


class MockedTestCase(TestCase):
    def setUp(self):
        self.avis1 = User.objects.create_user(
            'avis1', 'avis1@email.it', 'avis1')

    def authenticate(self, username, password):
        response = self.client.post('/api/token/', {
            'username': username,
            'password': password,
        })
        self.access_token = response.data['access']
        self.refresh_token = response.data['refresh']
