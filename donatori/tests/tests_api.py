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


class SezioneViewSetTestCase(MockedTestCase):
    def test_get_sezioni_empty(self):
        self.client.force_login(self.avis1)
        response = self.client.get('/api/sezioni/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])

    def test_get_sezioni(self):
        self.client.force_login(self.avis2)
        response = self.client.get('/api/sezioni/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertDictContainsSubset({
            'descrizione': 'AVIS 2',
            'ragione_sociale': 'AVIS ABC',
            'indirizzo': 'Via Roma 12',
        }, response.data[0])

        response = self.client.get(
            '/api/sezioni/{}/'.format(response.data[0]['id']))
        self.assertEqual(response.status_code, 200)
        self.assertDictContainsSubset({
            'descrizione': 'AVIS 2',
            'ragione_sociale': 'AVIS ABC',
            'indirizzo': 'Via Roma 12',
        }, response.data)

    def test_post_sezione(self):
        self.client.force_login(self.avis2)
        response = self.client.post('/api/sezioni/')
        self.assertEqual(response.status_code, 405)

    def test_put_sezione(self):
        self.client.force_login(self.avis2)
        response = self.client.get('/api/sezioni/')
        id_sezione = response.data[0]['id']
        new_sezione = {
            'id': id_sezione,
            'descrizione': 'AVIS 2 new',
            'ragione_sociale': 'AVIS DEF',
        }
        response = self.client.put(
            '/api/sezioni/{}/'.format(id_sezione), new_sezione)
        self.assertEqual(response.status_code, 200)
        self.assertDictContainsSubset({
            'descrizione': 'AVIS 2 new',
            'ragione_sociale': 'AVIS DEF',
            'indirizzo': 'Via Roma 12',
        }, response.data)

    def test_patch_sezione(self):
        self.client.force_login(self.avis2)
        response = self.client.get('/api/sezioni/')
        id_sezione = response.data[0]['id']
        new_sezione = {
            'descrizione': 'AVIS 2 new',
            'ragione_sociale': 'AVIS DEF',
        }
        response = self.client.patch(
            '/api/sezioni/{}/'.format(id_sezione), new_sezione)
        self.assertEqual(response.status_code, 200)
        self.assertDictContainsSubset({
            'descrizione': 'AVIS 2 new',
            'ragione_sociale': 'AVIS DEF',
            'indirizzo': 'Via Roma 12',
        }, response.data)

    def test_patch_sezione(self):
        self.client.force_login(self.avis2)
        response = self.client.get('/api/sezioni/')
        id_sezione = response.data[0]['id']
        new_sezione = {
            'descrizione': 'AVIS 2 new',
        }
        response = self.client.patch(
            '/api/sezioni/{}/'.format(id_sezione), new_sezione)
        self.assertEqual(response.status_code, 200)
        self.assertDictContainsSubset({
            'descrizione': 'AVIS 2 new',
            'ragione_sociale': 'AVIS ABC',
            'indirizzo': 'Via Roma 12',
        }, response.data)

    def test_delete_sezione(self):
        self.client.force_login(self.avis2)
        response = self.client.get('/api/sezioni/')
        id_sezione = response.data[0]['id']
        response = self.client.delete('/api/sezioni/{}/'.format(id_sezione))
        self.assertEqual(response.status_code, 405)
