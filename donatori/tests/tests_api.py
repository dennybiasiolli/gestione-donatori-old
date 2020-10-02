from django.contrib.auth.models import User

from .mocked_data import MockedTestCase


class CurrentUserViewSetTestCase(MockedTestCase):
    def test_get_userprofile(self):
        self.client.force_login(self.avis1)
        response = self.client.get('/api/me/')
        self.assertEqual(response.status_code, 200)
        self.assertDictContainsSubset({
            'email': 'avis1@email.it',
            'sezione': None,
        }, response.data)

        self.client.force_login(self.avis2)
        response = self.client.get('/api/me/')
        self.assertEqual(response.status_code, 200)
        self.assertDictContainsSubset({
            'email': 'avis2@email.it',
            'sezione': {
                'descrizione': 'AVIS 2',
            },
        }, response.data)
