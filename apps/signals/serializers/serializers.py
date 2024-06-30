from rest_framework import serializers
from ..models import Unit, Lessons, UUnit, ULesson, UserResponse

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
    show_for_my_level = serializers.SerializerMethodField()

    class Meta:
        model = Unit
        fields = ['id', 'name', 'level', 'show_for_my_level']

    def get_show_for_my_level(self, obj):
        request = self.context.get('request')
        user = request.user if request and hasattr(request, 'user') else None
        if obj.level >= user.level:
            return True
        return False
    
    def create(self, validated_data):
        unit = Unit.objects.create(**validated_data)
        return unit
    

class UserResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserResponse
        fields = ['id', 'lesson', 'response', 'correct', 'time_taken']