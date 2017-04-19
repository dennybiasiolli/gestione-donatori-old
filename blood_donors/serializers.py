from rest_framework import serializers

from .models import Sezione


class SezioneSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Sezione
        fields = ('__all__')
