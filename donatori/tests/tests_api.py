from datetime import date
from django.contrib.auth.models import User

from donatori.models import Donazione
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


class StatoDonatoreViewSetTestCase(MockedTestCase):
    def test_get_stati_donatore(self):
        self.client.force_login(self.avis1)
        response = self.client.get('/api/stati-donatore/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertListEqual(response.data, [
            {
                'id': 1,
                'codice': 'Attivo',
                'descrizione': 'Attivo',
                'is_attivo': True,
                'utente': None,
            },
            {
                'id': 2,
                'codice': 'Inattivo',
                'descrizione': 'Inattivo',
                'is_attivo': False,
                'utente': None,
            },
        ])

        self.client.force_login(self.avis2)
        response = self.client.get('/api/stati-donatore/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 4)

    def test_get_stato_donatore(self):
        self.client.force_login(self.avis1)
        response = self.client.get(
            '/api/stati-donatore/{}/'.format(self.stato_c1.id))
        self.assertEqual(response.status_code, 404)

        self.client.force_login(self.avis2)
        response = self.client.get(
            '/api/stati-donatore/{}/'.format(self.stato_c1.id))
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.data, {
            'id': self.stato_c1.id,
            'codice': 'C1',
            'descrizione': 'Custom 1',
            'is_attivo': True,
            'utente': self.avis2.id,
        })

    def test_post_stato_donatore(self):
        self.client.force_login(self.avis1)
        response = self.client.post('/api/stati-donatore/', {
            'codice': 'C1',
        })
        self.assertEqual(response.status_code, 201)
        self.assertDictContainsSubset({
            'codice': 'C1',
            'descrizione': '',
            'is_attivo': True,
            'utente': self.avis1.id,
        }, response.data)

        response = self.client.post('/api/stati-donatore/', {
            'codice': 'C1',
        })
        self.assertEqual(response.status_code, 400)

    def test_put_stato_donatore(self):
        self.client.force_login(self.avis1)
        response = self.client.put(
            '/api/stati-donatore/{}/'.format(self.stato_c1.id))
        self.assertEqual(response.status_code, 404)

        self.client.force_login(self.avis2)
        response = self.client.put(
            '/api/stati-donatore/{}/'.format(self.stato_c1.id), {
                'codice': 'C1 new',
            })
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.data, {
            'id': self.stato_c1.id,
            'codice': 'C1 new',
            'descrizione': 'Custom 1',
            'is_attivo': True,
            'utente': self.avis2.id,
        })

    def test_patch_stato_donatore(self):
        self.client.force_login(self.avis1)
        response = self.client.patch(
            '/api/stati-donatore/{}/'.format(self.stato_c1.id))
        self.assertEqual(response.status_code, 404)

        self.client.force_login(self.avis2)
        response = self.client.patch(
            '/api/stati-donatore/{}/'.format(self.stato_c1.id), {
                'descrizione': 'ciao',
            })
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.data, {
            'id': self.stato_c1.id,
            'codice': 'C1',
            'descrizione': 'ciao',
            'is_attivo': True,
            'utente': self.avis2.id,
        })

    def test_delete_stato_donatore(self):
        self.client.force_login(self.avis1)
        response = self.client.delete('/api/stati-donatore/1/')
        self.assertEqual(response.status_code, 404)
        response = self.client.delete(
            '/api/stati-donatore/{}/'.format(self.stato_c1.id))
        self.assertEqual(response.status_code, 404)

        self.client.force_login(self.avis2)
        response = self.client.delete('/api/stati-donatore/1/')
        self.assertEqual(response.status_code, 404)
        response = self.client.delete(
            '/api/stati-donatore/{}/'.format(self.stato_c1.id))
        self.assertEqual(response.status_code, 204)


class DonatoreViewSetTestCase(MockedTestCase):
    def test_get_donatori(self):
        self.client.force_login(self.avis1)
        response = self.client.get('/api/donatori/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

        self.client.force_login(self.avis2)
        response = self.client.get('/api/donatori/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertDictEqual(response.data[0], {
            'sezione_id': self.sezione1.id,
            'id': 1,
            'num_tessera': '0001',
            'cognome': 'Rossi',
            'nome': 'Mario',
            'sesso_id': 1,
            'stato_donatore_id': 1,
        })

    def test_get_donatore(self):
        self.client.force_login(self.avis1)
        response = self.client.get(
            '/api/donatori/{}/'.format(self.donatore1.id))
        self.assertEqual(response.status_code, 404)

        self.client.force_login(self.avis2)
        response = self.client.get(
            '/api/donatori/{}/'.format(self.donatore1.id))
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.data, {
            'id': 1,
            'sezione': {
                'id': self.sezione1.id,
                'descrizione': self.sezione1.descrizione,
                'ragione_sociale': self.sezione1.ragione_sociale,
                'indirizzo': self.sezione1.indirizzo,
                'frazione': self.sezione1.frazione,
                'cap': self.sezione1.cap,
                'citta': self.sezione1.citta,
                'provincia': self.sezione1.provincia,
                'tel': self.sezione1.tel,
                'fax': self.sezione1.fax,
                'email': self.sezione1.email,
                'presidente': self.sezione1.presidente,
                'segretario': self.sezione1.segretario,
            },
            'num_tessera': '0001',
            'cognome': 'Rossi',
            'nome': 'Mario',
            'sesso': {
                'id': self.sesso_m.id,
                'codice': self.sesso_m.codice,
                'descrizione': self.sesso_m.descrizione,
            },
            'stato_donatore': {
                'id': self.stato_attivo.id,
                'codice': self.stato_attivo.codice,
                'descrizione': self.stato_attivo.descrizione,
                'is_attivo': self.stato_attivo.is_attivo,
                'utente': self.stato_attivo.utente,
            },
            'num_tessera_cartacea': '',
            'data_rilascio_tessera': None,
            'codice_fiscale': 'ABCDEF',
            'data_nascita': None,
            'data_iscrizione': None,
            'gruppo_sanguigno': '',
            'rh': '',
            'fenotipo': '',
            'kell': '',
            'indirizzo': '',
            'frazione': '',
            'cap': '',
            'citta': '',
            'provincia': '',
            'tel': '',
            'tel_lavoro': '',
            'cell': '',
            'fax': '',
            'email': '',
            'fermo_per_malattia': False,
            'donazioni_pregresse': 0,
            'num_benemerenze': 0,
            'donazioni': [{
                'id': self.donazione1.id,
                'tipo_donazione': self.donazione1.tipo_donazione,
                'data_donazione': self.donazione1.data_donazione.strftime('%Y-%m-%d'),
            }],
        })

    def test_post_donatore(self):
        self.client.force_login(self.avis1)
        response = self.client.post('/api/donatori/', {
            'sezione_id': self.sezione1.id,
            'num_tessera': '0003',
            'cognome': 'Verdi',
            'nome': 'Luigi',
            'sesso_id': self.sesso_m.id,
            'stato_donatore_id': self.stato_attivo.id,
        })
        self.assertEqual(response.status_code, 400)

        self.client.force_login(self.avis2)
        response = self.client.post('/api/donatori/', {
            'sezione_id': self.sezione1.id,
            'num_tessera': '0001',
            'cognome': 'Verdi',
            'nome': 'Luigi',
            'sesso_id': self.sesso_m.id,
            'stato_donatore_id': self.stato_attivo.id,
        })
        self.assertEqual(response.status_code, 400)

        self.client.force_login(self.avis2)
        response = self.client.post('/api/donatori/', {
            'sezione_id': self.sezione1.id,
            'num_tessera': '0003',
            'cognome': 'Verdi',
            'nome': 'Luigi',
            'sesso_id': self.sesso_m.id,
            'stato_donatore_id': self.stato_attivo.id,
            'codice_fiscale': 'CIAO',
        })
        self.assertEqual(response.status_code, 201)
        self.assertDictContainsSubset({
            'sezione_id': self.sezione1.id,
            'num_tessera': '0003',
            'cognome': 'Verdi',
            'nome': 'Luigi',
            'sesso_id': self.sesso_m.id,
            'stato_donatore_id': self.stato_attivo.id,
            'codice_fiscale': 'CIAO',
        }, response.data)

    def test_put_donatore(self):
        self.client.force_login(self.avis1)
        response = self.client.put(
            '/api/donatori/{}/'.format(self.donatore1.id))
        self.assertEqual(response.status_code, 404)

        self.client.force_login(self.avis2)
        response = self.client.put(
            '/api/donatori/{}/'.format(self.donatore1.id), {
                'sezione_id': self.sezione1.id,
                'num_tessera': self.donatore1.num_tessera,
                'cognome': self.donatore1.cognome,
                'nome': self.donatore1.nome,
                'sesso_id': self.donatore1.sesso.id,
                'stato_donatore_id': self.stato_inattivo.id,
                'frazione': 'fooooo',
            })
        self.assertEqual(response.status_code, 200)
        self.assertDictContainsSubset({
            'sezione_id': self.sezione1.id,
            'id': 1,
            'num_tessera': '0001',
            'cognome': 'Rossi',
            'nome': 'Mario',
            'sesso_id': self.sesso_m.id,
            'stato_donatore_id': self.stato_inattivo.id,
            'codice_fiscale': 'ABCDEF',
            'frazione': 'fooooo',
        }, response.data)

    def test_patch_donatore(self):
        self.client.force_login(self.avis1)
        response = self.client.patch(
            '/api/donatori/{}/'.format(self.donatore1.id))
        self.assertEqual(response.status_code, 404)

        self.client.force_login(self.avis2)
        response = self.client.patch(
            '/api/donatori/{}/'.format(self.donatore1.id), {
                'cap': '12345',
            })
        self.assertEqual(response.status_code, 200)
        self.assertDictContainsSubset({
            'sezione_id': self.sezione1.id,
            'id': 1,
            'num_tessera': '0001',
            'cognome': 'Rossi',
            'nome': 'Mario',
            'sesso_id': self.sesso_m.id,
            'stato_donatore_id': self.stato_attivo.id,
            'codice_fiscale': 'ABCDEF',
            'cap': '12345',
        }, response.data)

    def test_delete_donatore(self):
        self.client.force_login(self.avis1)
        response = self.client.delete(
            '/api/donatori/{}/'.format(self.donatore1.id))
        self.assertEqual(response.status_code, 404)

        self.client.force_login(self.avis2)
        response = self.client.delete(
            '/api/donatori/{}/'.format(self.donatore1.id))
        self.assertEqual(response.status_code, 204)


class DonazioneViewSetTestCase(MockedTestCase):
    def test_get_donazioni(self):
        self.client.force_login(self.avis1)
        response = self.client.get('/api/donazioni/')
        self.assertEqual(response.status_code, 405)

    def test_get_donazione(self):
        self.client.force_login(self.avis1)
        response = self.client.get(
            '/api/donazioni/{}/'.format(self.donazione1.id))
        self.assertEqual(response.status_code, 404)

        self.client.force_login(self.avis2)
        response = self.client.get(
            '/api/donazioni/{}/'.format(self.donazione1.id))
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.data, {
            'id': self.donazione1.id,
            'donatore_id': self.donazione1.donatore.id,
            'tipo_donazione': self.donazione1.tipo_donazione,
            'data_donazione': self.donazione1.data_donazione.strftime('%Y-%m-%d'),
        })

    def test_post_donazione(self):
        self.client.force_login(self.avis1)
        response = self.client.post('/api/donazioni/', {
            'donatore_id': self.donatore1.id,
            'tipo_donazione': Donazione.PLASMA,
        })
        self.assertEqual(response.status_code, 400)

        self.client.force_login(self.avis2)
        response = self.client.post('/api/donazioni/', {
            'donatore_id': self.donatore1.id,
            'tipo_donazione': Donazione.PLASMA,
            'data_donazione': date(2020, 10, 1),
        })
        self.assertEqual(response.status_code, 201)
        self.assertDictContainsSubset({
            'donatore_id': self.donatore1.id,
            'tipo_donazione': Donazione.PLASMA,
            'data_donazione': date(2020, 10, 1).strftime('%Y-%m-%d'),
        }, response.data)
        response = self.client.post('/api/donazioni/', {
            'donatore_id': self.donatore1.id,
            'tipo_donazione': Donazione.PLASMA,
            'data_donazione': date(2020, 10, 1),
        })
        self.assertEqual(response.status_code, 400)

    def test_put_donazione(self):
        self.client.force_login(self.avis1)
        response = self.client.put(
            '/api/donazioni/{}/'.format(self.donazione1.id))
        self.assertEqual(response.status_code, 404)

        self.client.force_login(self.avis2)
        response = self.client.put(
            '/api/donazioni/{}/'.format(self.donazione1.id), {
                'donatore_id': self.donatore1.id,
                'tipo_donazione': Donazione.PIASTRINE,
                'data_donazione': date(2020, 10, 1),
            })
        self.assertEqual(response.status_code, 200)
        self.assertDictContainsSubset({
            'donatore_id': self.donatore1.id,
            'tipo_donazione': Donazione.PIASTRINE,
            'data_donazione': date(2020, 10, 1).strftime('%Y-%m-%d'),
        }, response.data)

    def test_patch_donazione(self):
        self.client.force_login(self.avis1)
        response = self.client.patch(
            '/api/donazioni/{}/'.format(self.donazione1.id))
        self.assertEqual(response.status_code, 404)

        self.client.force_login(self.avis2)
        response = self.client.patch(
            '/api/donazioni/{}/'.format(self.donazione1.id), {
                'tipo_donazione': Donazione.PLASMA,
            })
        self.assertEqual(response.status_code, 200)
        self.assertDictContainsSubset({
            'donatore_id': self.donatore1.id,
            'tipo_donazione': Donazione.PLASMA,
            'data_donazione': date(2020, 10, 11).strftime('%Y-%m-%d'),
        }, response.data)

    def test_delete_donazione(self):
        self.client.force_login(self.avis1)
        response = self.client.delete(
            '/api/donazioni/{}/'.format(self.donazione1.id))
        self.assertEqual(response.status_code, 404)

        self.client.force_login(self.avis2)
        response = self.client.delete(
            '/api/donazioni/{}/'.format(self.donazione1.id))
        self.assertEqual(response.status_code, 204)
