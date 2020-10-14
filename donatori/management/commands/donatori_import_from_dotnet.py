# -*- coding: utf-8 -*-
import datetime
import json
import os
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q

from donatori.models import (
    Donatore,
    Donazione,
    Sesso,
    Sezione,
    StatoDonatore,
)


class Command(BaseCommand):
    help = 'Importa gli ambiti nel gestionale'

    def add_arguments(self, parser):
        parser.add_argument('-d', '--dir', type=str, required=True,
                            help='path containing files to import')

    def _read_json(self, path):
        with open(path) as f:
            return json.load(f)

    def _date_from_string_or_none(self, str_datetime):
        return str_datetime[:10] if str_datetime else None

    def handle(self, *args, **options):
        # import users/sezioni
        sezioni = self._read_json(os.path.join(
            options['dir'], 'sezioni.json'))
        for s in sezioni:
            user = User.objects.filter(email=s['Email']).first()
            if user is None:
                user = User.objects.create_user(
                    username=s['Email'],
                    email=s['Email'],
                    password=s['Email'],
                )
            sez = Sezione.objects.filter(descrizione=s['Descrizione']).first()
            if sez is None:
                sez = Sezione.objects.create(
                    utente=user,
                    descrizione=s['Descrizione'],
                    ragione_sociale=s['Descrizione'],
                    indirizzo=s['Indirizzo'],
                    frazione=s['Frazione'],
                    cap=s['Cap'],
                    citta=s['Comune'],
                    provincia=s['Provincia'],
                    tel=s['Tel'],
                    fax=s['Fax'],
                    email=s['Email'],
                    presidente=s['Presidente'],
                    segretario=s['Segretario'],
                )

            # import stati donatori
            stati = self._read_json(os.path.join(
                options['dir'], 'statiDonatori.json'))
            for stato in stati:
                stato_donatore = StatoDonatore.objects.filter(
                    # utente=user,
                    codice=stato['Descrizione'],
                ).first()
                if stato_donatore is None:
                    stato_donatore = StatoDonatore.objects.create(
                        utente=user,
                        codice=stato['Descrizione'],
                        descrizione=stato['DescrizioneEstesa'],
                        is_attivo=stato['Attivo'],
                    )

            stati_donatore = StatoDonatore.objects.filter(
                Q(utente__isnull=True) | Q(utente=user)
            ).values('id', 'codice')

            # import donatori
            donatori = self._read_json(os.path.join(
                options['dir'], 'donatori.json'))
            sesso_m = Sesso.objects.filter(codice='M').first()
            sesso_f = Sesso.objects.filter(codice='F').first()
            for d in donatori:
                donatore = Donatore.objects.filter(
                    sezione=sez,
                    num_tessera=d['NumTessera'],
                ).first()
                if donatore is None:
                    sesso = d.get('Sesso', {}) or {}
                    sesso = sesso.get('Descrizione', 'F')
                    sesso = sesso_f if sesso == 'F' else sesso_m
                    donatore = Donatore.objects.create(
                        sezione=sez,
                        num_tessera=d['NumTessera'],
                        cognome=d['Cognome'],
                        nome=d['Nome'],
                        sesso=sesso,
                        stato_donatore_id=stati_donatore.filter(
                            codice=d['StatoDonatore']['Descrizione']).first()['id'],
                        num_tessera_cartacea=d['NumTesseraCartacea'] or '',
                        data_rilascio_tessera=self._date_from_string_or_none(
                            d['DataRilascioTessera']),
                        codice_fiscale='',
                        data_nascita=self._date_from_string_or_none(
                            d['DataNascita']),
                        data_iscrizione=self._date_from_string_or_none(
                            d['DataIscrizione']),
                        gruppo_sanguigno=d['GruppoSanguigno'],
                        rh=d['Rh'],
                        fenotipo=d['Fenotipo'],
                        kell=d['Kell'],
                        indirizzo=d['Indirizzo'],
                        frazione=d['Frazione'],
                        cap=d['Cap'],
                        citta=d['Comune'],
                        provincia=d['Provincia'],
                        tel=d['Telefono'],
                        tel_lavoro=d['TelefonoLavoro'],
                        cell=d['Cellulare'],
                        fax='',
                        email=d['Email'],
                        fermo_per_malattia=d['FermoPerMalattia'],
                        donazioni_pregresse=d['DonazioniPregresse'],
                        num_benemerenze=d['NumBenemerenze'],
                    )

                # import donazioni
                donazioni = sorted(
                    d['donazioni'], key=lambda k: k['DataDonazione'])
                for donazione in donazioni:
                    tipo_donazione = donazione.get('TipoDonazione', {}) or {}
                    tipo_donazione = tipo_donazione.get('Descrizione', None)
                    if tipo_donazione == 'Sangue intero':
                        tipo_donazione = Donazione.SANGUE_INTERO
                    elif tipo_donazione == 'Plasma':
                        tipo_donazione = Donazione.PLASMA
                    elif tipo_donazione is None:
                        tipo_donazione = Donazione.NON_SPECIFICATO
                    else:
                        print(tipo_donazione)
                        raise tipo_donazione
                    try:
                        Donazione.objects.create(
                            donatore=donatore,
                            tipo_donazione=tipo_donazione,
                            data_donazione=self._date_from_string_or_none(
                                donazione['DataDonazione']),
                        )
                    except Exception as err:
                        print(
                            donatore,
                            '\n',
                            '\t',
                            self._date_from_string_or_none(
                                donazione['DataDonazione']),
                            # err,
                        )

        self.stdout.write('Importazione donatori completata con successo')
