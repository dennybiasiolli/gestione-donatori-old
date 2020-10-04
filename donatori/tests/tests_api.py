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
        new_sezione = {
            'id': self.sezione1.id,
            'descrizione': 'AVIS 2 new',
            'ragione_sociale': 'AVIS DEF',
        }
        response = self.client.put(
            '/api/sezioni/{}/'.format(self.sezione1.id), new_sezione)
        self.assertEqual(response.status_code, 200)
        self.assertDictContainsSubset({
            'descrizione': 'AVIS 2 new',
            'ragione_sociale': 'AVIS DEF',
            'indirizzo': 'Via Roma 12',
        }, response.data)

    def test_patch_sezione(self):
        self.client.force_login(self.avis2)
        new_sezione = {
            'descrizione': 'AVIS 2 new',
            'ragione_sociale': 'AVIS DEF',
        }
        response = self.client.patch(
            '/api/sezioni/{}/'.format(self.sezione1.id), new_sezione)
        self.assertEqual(response.status_code, 200)
        self.assertDictContainsSubset({
            'descrizione': 'AVIS 2 new',
            'ragione_sociale': 'AVIS DEF',
            'indirizzo': 'Via Roma 12',
        }, response.data)

    def test_patch_sezione(self):
        self.client.force_login(self.avis2)
        new_sezione = {
            'descrizione': 'AVIS 2 new',
        }
        response = self.client.patch(
            '/api/sezioni/{}/'.format(self.sezione1.id), new_sezione)
        self.assertEqual(response.status_code, 200)
        self.assertDictContainsSubset({
            'descrizione': 'AVIS 2 new',
            'ragione_sociale': 'AVIS ABC',
            'indirizzo': 'Via Roma 12',
        }, response.data)

    def test_delete_sezione(self):
        self.client.force_login(self.avis2)
        response = self.client.delete(
            '/api/sezioni/{}/'.format(self.sezione1.id))
        self.assertEqual(response.status_code, 405)


class SessoViewSetTestCase(MockedTestCase):
    def test_get_sessi(self):
        self.client.force_login(self.avis1)
        response = self.client.get('/api/sessi/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertListEqual(response.data, [
            {
                'id': 1,
                'codice': 'M',
                'descrizione': 'Maschio',
            },
            {
                'id': 2,
                'codice': 'F',
                'descrizione': 'Femmina',
            },
        ])

    def test_get_sesso(self):
        self.client.force_login(self.avis1)
        response = self.client.get('/api/sessi/1/')
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.data, {
            'id': 1,
            'codice': 'M',
            'descrizione': 'Maschio',
            'gg_da_sangue_a_sangue': 90,
            'gg_da_sangue_a_plasma': 30,
            'gg_da_sangue_a_piastrine': 30,
            'gg_da_plasma_a_sangue': 14,
            'gg_da_plasma_a_plasma': 14,
            'gg_da_plasma_a_piastrine': 14,
            'gg_da_piastrine_a_sangue': 14,
            'gg_da_piastrine_a_plasma': 30,
            'gg_da_piastrine_a_piastrine': 30,
        })
        response = self.client.get('/api/sessi/2/')
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.data, {
            'id': 2,
            'codice': 'F',
            'descrizione': 'Femmina',
            'gg_da_sangue_a_sangue': 180,
            'gg_da_sangue_a_plasma': 30,
            'gg_da_sangue_a_piastrine': 30,
            'gg_da_plasma_a_sangue': 14,
            'gg_da_plasma_a_plasma': 14,
            'gg_da_plasma_a_piastrine': 14,
            'gg_da_piastrine_a_sangue': 14,
            'gg_da_piastrine_a_plasma': 30,
            'gg_da_piastrine_a_piastrine': 30,
        })

    def test_post_sesso(self):
        self.client.force_login(self.avis1)
        response = self.client.post('/api/sessi/')
        self.assertEqual(response.status_code, 405)

    def test_put_sesso(self):
        self.client.force_login(self.avis1)
        response = self.client.get('/api/sessi/')
        id = response.data[0]['id']
        response = self.client.put('/api/sessi/{}/'.format(id))
        self.assertEqual(response.status_code, 405)

    def test_patch_sesso(self):
        self.client.force_login(self.avis1)
        response = self.client.get('/api/sessi/')
        id = response.data[0]['id']
        response = self.client.patch('/api/sessi/{}/'.format(id))
        self.assertEqual(response.status_code, 405)

    def test_delete_sesso(self):
        self.client.force_login(self.avis1)
        response = self.client.get('/api/sessi/')
        id = response.data[0]['id']
        response = self.client.delete('/api/sessi/{}/'.format(id))
        self.assertEqual(response.status_code, 405)
