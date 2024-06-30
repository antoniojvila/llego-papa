from rest_framework import serializers
from ..models import Unit, Lessons, UUnit, ULesson

class UUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = UUnit
        fields = ['id', 'name', 'user', 'average', 'createdAt', 'updatedAt']

class ULessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = ULesson
        fields = ['id', 'user', 'name', 'image', 'video', 'unit', 'completed', 'createdAt', 'updatedAt']

class LessonsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lessons
        fields = ['id', 'name', 'image', 'video', 'unit']

class UnitSerializer(serializers.ModelSerializer):

    class Meta:
        model = Unit
        fields = ['id', 'name']

    def create(self, validated_data):
        unit = Unit.objects.create(**validated_data)
        return unit