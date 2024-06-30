from rest_framework import serializers
from ..models import Score, RoundHistory

class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = ['score']

class RoundHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RoundHistory
        fields = ['hits', 'errors', 'game', 'time', 'created_at']
        read_only_fields = ['created_at']