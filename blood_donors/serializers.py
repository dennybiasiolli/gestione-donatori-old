from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import serializers

from .models import (Sezione, CentroDiRaccolta, Sesso,
                     StatoDonatore, TipoDonazione, Donatore)


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ('url', 'username', 'email',
                  'is_superuser', 'first_name', 'last_name')


class SezioneSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Sezione
        fields = ('url', 'id', 'descrizione', 'indirizzo', 'frazione',
                  'cap', 'citta', 'provincia', 'tel', 'fax', 'email', )


class SezioneChildSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Sezione
        fields = ('url', 'id', 'descrizione')


class CentroDiRaccoltaSerializer(serializers.HyperlinkedModelSerializer):
    owner = UserSerializer(read_only=True)

    class Meta:
        model = CentroDiRaccolta
        fields = ('__all__')


class CentroDiRaccoltaChildSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = CentroDiRaccolta
        fields = ('url', 'id', 'descrizione')


class SessoSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Sesso
        fields = ('__all__')


class SessoChildSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Sesso
        fields = ('url', 'id', 'descrizione')


class StatoDonatoreSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = StatoDonatore
        fields = ('__all__')


class TipoDonazioneSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = TipoDonazione
        fields = ('__all__')


class DonatoreSerializer(serializers.HyperlinkedModelSerializer):
    # sezione = SezioneChildSerializer(read_only=False,
    #     style={'base_template': 'select.html'}
    # )
    sezione_id = serializers.PrimaryKeyRelatedField(
        read_only=False,
        queryset=Sezione.objects.all(),
        source='sezione')
    sezione = SezioneChildSerializer(read_only=True)
    sesso_id = serializers.PrimaryKeyRelatedField(
        read_only=False,
        queryset=Sesso.objects.all(),
        source='sesso')
    sesso = SessoChildSerializer(read_only=True)
    stato_donatore_id = serializers.PrimaryKeyRelatedField(
        read_only=False,
        queryset=StatoDonatore.objects.all(),
        source='stato_donatore')
    stato_donatore = StatoDonatoreSerializer(read_only=True)
    centro_raccolta_default_id = serializers.PrimaryKeyRelatedField(
        read_only=False,
        queryset=CentroDiRaccolta.objects.all(),
        source='centro_raccolta_default',
        allow_null=True)
    centro_raccolta_default = CentroDiRaccoltaChildSerializer(
        read_only=True)

    class Meta:
        model = Donatore
        fields = ('url', 'id', 'sezione_id', 'sezione', 'num_tessera',
                  'num_tessera_cartacea', 'data_rilascio_tessera', 'cognome',
                  'nome', 'codice_fiscale', 'sesso_id', 'sesso', 'data_nascita',
                  'data_iscrizione', 'stato_donatore_id', 'stato_donatore',
                  'gruppo_sanguigno', 'rh', 'fenotipo', 'kell', 'indirizzo',
                  'frazione', 'cap', 'citta', 'provincia', 'tel', 'tel_lavoro',
                  'cell', 'fax', 'email', 'fermo_per_malattia',
                  'donazioni_pregresse', 'num_benemerenze',
                  'centro_raccolta_default_id', 'centro_raccolta_default',)
        depth = 1

    def __init__(self, *args, **kwargs):
        # Make sure that self.fields is populated
        super().__init__(*args, **kwargs)

        # Filtering related querysets to current user
        user = self.context['request'].user
        self.fields['sezione_id'].queryset = Sezione.objects.filter(
            owner=user)
        self.fields['stato_donatore_id'].queryset = StatoDonatore.objects.filter(
            Q(owner=user) | Q(owner=None))
        self.fields['centro_raccolta_default_id'].queryset = CentroDiRaccolta.objects.filter(
            owner=user)

    def validate_sezione(self, value):
        if value.owner != self.context['request'].user:
            raise serializers.ValidationError('Sezione non esistente')
        return value

    def validate_centro_raccolta_default(self, value):
        if value and value.owner != self.context['request'].user:
            raise serializers.ValidationError(
                'Centro di raccolta non esistente')
        return value
