from django.test import TestCase


class APIUnauthenticatedTestCase(TestCase):
    def test_get_userprofile(self):
        response = self.client.get('/api/me/')
        self.assertEqual(response.status_code, 403)
