from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Sezione


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
