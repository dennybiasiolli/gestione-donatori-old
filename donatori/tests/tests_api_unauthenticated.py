from django.test import TestCase


class APIUnauthenticatedTestCase(TestCase):
    def test_get_userprofile(self):
        response = self.client.get('/api/me/')
        self.assertEqual(response.status_code, 403)

    def test_get_sezioni(self):
        response = self.client.get('/api/sezioni/')
        self.assertEqual(response.status_code, 403)

    def test_get_sessi(self):
        response = self.client.get('/api/sessi/')
        self.assertEqual(response.status_code, 403)
