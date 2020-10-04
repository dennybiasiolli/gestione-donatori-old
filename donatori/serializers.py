from django.contrib.auth.models import User
from rest_framework import serializers

from .models import (
    Sesso,
    Sezione,
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
