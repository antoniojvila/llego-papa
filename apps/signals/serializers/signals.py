from rest_framework import serializers
from ..models import Signals

class SignalsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Signals
        fields = ['id', 'name', 'value', 'meaning']