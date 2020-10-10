from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import (
    Donatore,
    Sesso,
    Sezione,
    StatoDonatore,
)


class SezioneSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Sezione
        fields = (
            'id',
            'descrizione', 'ragione_sociale', 'indirizzo', 'frazione', 'cap',
            'citta', 'provincia', 'tel', 'fax', 'email',
            'presidente', 'segretario',
        )


class SezioneUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Sezione
        fields = ('descrizione',)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    sezione = SezioneUserSerializer()

    class Meta:
        model = User
        fields = ('id', 'email', 'sezione',)


class SessoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Sesso
        fields = ('id', 'codice', 'descrizione')


class SessoDetailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Sesso
        fields = ('id', 'codice', 'descrizione',
                  'gg_da_sangue_a_sangue',
                  'gg_da_sangue_a_plasma',
                  'gg_da_sangue_a_piastrine',
                  'gg_da_plasma_a_sangue',
                  'gg_da_plasma_a_plasma',
                  'gg_da_plasma_a_piastrine',
                  'gg_da_piastrine_a_sangue',
                  'gg_da_piastrine_a_plasma',
                  'gg_da_piastrine_a_piastrine',
                  )


class StatoDonatoreSerializer(serializers.HyperlinkedModelSerializer):
    utente = serializers.PrimaryKeyRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )
    is_attivo = serializers.BooleanField(default=True)

    class Meta:
        model = StatoDonatore
        fields = ('id', 'codice', 'descrizione', 'is_attivo',
                  'utente')


class DonatoreListSerializer(serializers.HyperlinkedModelSerializer):
    sezione_id = serializers.PrimaryKeyRelatedField(read_only=True)
    sesso_id = serializers.PrimaryKeyRelatedField(read_only=True)
    stato_donatore_id = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Donatore
        fields = ('id', 'sezione_id',
                  'num_tessera', 'cognome', 'nome',
                  'sesso_id',
                  'stato_donatore_id',
                  )


class DonatoreSerializer(serializers.HyperlinkedModelSerializer):
    sezione_id = serializers.PrimaryKeyRelatedField(
        queryset=Sezione.objects.all(),
        source='sezione',
    )
    sesso_id = serializers.PrimaryKeyRelatedField(
        queryset=Sesso.objects.all(),
        source='sesso',
    )
    stato_donatore_id = serializers.PrimaryKeyRelatedField(
        queryset=StatoDonatore.objects.all(),
        source='stato_donatore',
    )

    class Meta:
        model = Donatore
        fields = ('id', 'sezione_id',
                  'num_tessera', 'cognome', 'nome',
                  'sesso_id',
                  'stato_donatore_id',
                  'num_tessera_cartacea',
                  'data_rilascio_tessera',
                  'codice_fiscale',
                  'data_nascita',
                  'data_iscrizione',
                  'gruppo_sanguigno',
                  'rh',
                  'fenotipo',
                  'kell',
                  'indirizzo',
                  'frazione',
                  'cap',
                  'citta',
                  'provincia',
                  'tel',
                  'tel_lavoro',
                  'cell',
                  'fax',
                  'email',
                  'fermo_per_malattia',
                  'donazioni_pregresse',
                  'num_benemerenze',
                  )

    def __init__(self, *args, **kwargs):
        super(DonatoreSerializer, self).__init__(*args, **kwargs)
        request_user = self.context['request'].user
        self.fields['sezione_id'].queryset = Sezione.objects.filter(
            utente=request_user
        )
        self.fields['stato_donatore_id'].queryset = StatoDonatore.objects.filter(
            Q(utente__isnull=True) | Q(utente=request_user)
        )
