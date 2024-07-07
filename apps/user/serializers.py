from rest_framework import serializers
from .models import User
from apps.signals.models import UUnit
from apps.score.models import Score
from apps.signals.serializers.serializers import UUnitSerializer
from apps.score.serializers.score import ScoreSerializer

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'birthday']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            birthday=validated_data.get('birthday'),
            role='alumno'
        )
        return user

class UserSerializer(serializers.ModelSerializer):
    units = serializers.SerializerMethodField()
    score = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['username', 'email', 'units', 'score']

    def get_units(self, obj):
        units = UUnit.objects.filter(user=obj)
        return UUnitSerializer(units, many=True).data

    def get_score(self, obj):
        score = Score.objects.filter(user=obj).order_by('id').last()
        if score:
            return ScoreSerializer(score).data
        return None