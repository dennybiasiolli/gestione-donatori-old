from django.contrib.auth.models import User
from django.test import TestCase


class APIAuthenticationTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            'user1', 'user1@email.it', 'user1')

    def _get_token(self):
        response = self.client.post('/api/token/', {
            'username': 'user1',
            'password': 'user1',
        })
        self.access_token = response.data['access']
        self.refresh_token = response.data['refresh']
        return response

    def test_get_token_wrong_credentials(self):
        response = self.client.post('/api/token/', {
            'username': 'user1',
            'password': 'user1_fail',
        })
        self.assertEqual(response.status_code, 401)

    def test_get_token(self):
        response = self._get_token()
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_verify_token(self):
        self._get_token()
        response = self.client.post('/api/token/verify/', {
            'token': self.access_token,
        })
        self.assertEqual(response.status_code, 200)
        response = self.client.post('/api/token/verify/', {
            'token': self.refresh_token,
        })
        self.assertEqual(response.status_code, 200)

    def test_refresh_token(self):
        self._get_token()
        response = self.client.post('/api/token/refresh/', {
            'refresh': self.refresh_token,
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_invalidate_old_refresh_tokens(self):
        self._get_token()
        old_refresh_token = self.refresh_token
        response = self.client.post('/api/token/refresh/', {
            'refresh': self.refresh_token,
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.access_token = response.data['access']
        self.refresh_token = response.data['refresh']
        self.assertNotEqual(self.refresh_token, old_refresh_token)
        response = self.client.post('/api/token/refresh/', {
            'refresh': old_refresh_token,
        })
        self.assertEqual(response.status_code, 401)
