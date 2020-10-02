from django.contrib.auth.models import User

from .mocked_data import MockedTestCase


class CurrentUserViewSetTestCase(MockedTestCase):
    def test_get_userprofile(self):
        self.client.force_login(self.avis1)
        response = self.client.get('/api/me/')
        self.assertEqual(response.status_code, 200)
        self.assertDictContainsSubset({
            'id': 1,
            'email': 'avis1@email.it',
            'profiloutente': {
                'is_sezione': False,
                'is_centro_di_raccolta': False,
                'is_donatore': False,
            },
        }, response.data)
