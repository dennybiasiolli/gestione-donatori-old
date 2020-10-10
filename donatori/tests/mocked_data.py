from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient

from donatori.models import (
    Donatore,
    Sesso,
    Sezione,
    StatoDonatore,
)


class MockedTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.avis1 = User.objects.create_user(
            'avis1', 'avis1@email.it', 'avis1')
        self.avis2 = User.objects.create_user(
            'avis2', 'avis2@email.it', 'avis2')
        self.avis3 = User.objects.create_user(
            'avis3', 'avis3@email.it', 'avis3')

        self.sezione1 = Sezione.objects.create(
            utente=self.avis2,
            descrizione='AVIS 2',
            ragione_sociale='AVIS ABC',
            indirizzo='Via Roma 12',
        )
        self.sezione2 = Sezione.objects.create(
            utente=self.avis3,
            descrizione='AVIS 3',
            ragione_sociale='AVIS VENEZIA',
            indirizzo='Corso Venezia 123',
        )
        self.stato_attivo = StatoDonatore.objects.filter(
            codice='Attivo', utente__isnull=True).first()
        self.stato_inattivo = StatoDonatore.objects.filter(
            codice='Inattivo', utente__isnull=True).first()
        self.stato_c1 = StatoDonatore.objects.create(
            utente=self.avis2,
            codice='C1',
            descrizione='Custom 1',
            is_attivo=True,
        )
        self.stato_c2 = StatoDonatore.objects.create(
            utente=self.avis2,
            codice='C2',
            descrizione='Custom 2',
            is_attivo=False,
        )

        self.sesso_m = Sesso.objects.filter(codice='M').first()
        self.sesso_f = Sesso.objects.filter(codice='F').first()

        self.donatore1 = Donatore.objects.create(
            sezione=self.sezione1,
            num_tessera='0001',
            cognome='Rossi',
            nome='Mario',
            sesso=self.sesso_m,
            stato_donatore=self.stato_attivo,
            codice_fiscale="ABCDEF",
        )
        self.donatore2 = Donatore.objects.create(
            sezione=self.sezione1,
            num_tessera='0002',
            cognome='Bianchi',
            nome='Paolo',
            sesso=self.sesso_m,
            stato_donatore=self.stato_attivo,
        )

    def authenticate(self, username, password):
        response = self.client.post('/api/token/', {
            'username': username,
            'password': password,
        })
        self.access_token = response.data['access']
        self.refresh_token = response.data['refresh']
