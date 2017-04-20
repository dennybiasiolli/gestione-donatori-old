from django.contrib.auth.models import User
from rest_framework import serializers

from .models import (Sezione, CentroDiRaccolta, Sesso,
                     StatoDonatore, TipoDonazione, Donatore)


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ('url', 'username', 'email',
                  'is_superuser', 'first_name', 'last_name')


class SezioneSerializer(serializers.HyperlinkedModelSerializer):
    owner = UserSerializer()

    class Meta:
        model = Sezione
        fields = ('__all__')


class CentroDiRaccoltaSerializer(serializers.HyperlinkedModelSerializer):
    owner = UserSerializer()

    class Meta:
        model = CentroDiRaccolta
        fields = ('__all__')


class SessoSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Sesso
        fields = ('__all__')


class StatoDonatoreSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = StatoDonatore
        fields = ('__all__')


class TipoDonazioneSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = TipoDonazione
        fields = ('__all__')


class DonatoreSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Donatore
        fields = ('url', 'id', 'sezione', 'num_tessera', 'num_tessera_cartacea',
                  'data_rilascio_tessera', 'cognome', 'nome', 'codice_fiscale',
                  'sesso', 'data_nascita', 'data_iscrizione', 'stato_donatore',
                  'gruppo_sanguigno', 'rh', 'fenotipo', 'kell', 'indirizzo',
                  'frazione', 'cap', 'citta', 'provincia', 'tel', 'tel_lavoro',
                  'cell', 'fax', 'email', 'fermo_per_malattia',
                  'donazioni_pregresse', 'num_benemerenze',
                  'centro_raccolta_default',)

    def __init__(self, *args, **kwargs):
        # Make sure that self.fields is populated
        super().__init__(*args, **kwargs)

        # Filtering related querysets to current user
        user = self.context['request'].user
        self.fields['sezione'].queryset = Sezione.objects.filter(
            owner=user)
        self.fields['centro_raccolta_default'].queryset = CentroDiRaccolta.objects.filter(
            owner=user)
