from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from .models import Unit
from .serializers.serializers import UnitSerializer, UUnitSerializer, ULessonSerializer
from .permissions import IsProfessor
from rest_framework.permissions import IsAuthenticated
from .models import Lessons
from .serializers.serializers import LessonsSerializer
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Unit, Lessons, UUnit, ULesson


class SignalsListView(APIView):
    def get(self, request, format=None):
        unit_id = request.query_params.get('unit_id')
        
        if not unit_id:
            return Response({'error': 'unit_id parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            unit_id = int(unit_id)
        except ValueError:
            return Response({'error': 'unit_id must be an integer'}, status=status.HTTP_400_BAD_REQUEST)
        
        signals = ULesson.objects.filter(unit__id=unit_id)
        signals_values = [
            {
                'id': signal.id,
                'image': request.build_absolute_uri(signal.ico.url) if signal.ico else None
            }
            for signal in signals
        ]
        responses_meanings = list(signals.values('id', 'name'))

        custom_response = {
            "signals": signals_values,
            "responses": responses_meanings
        }

        return Response(custom_response, status=status.HTTP_200_OK)

class UnitViewSet(viewsets.ModelViewSet):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer
    permission_classes = [IsAuthenticated, IsProfessor]
    ordering_fields = ['level', 'name']  # Opcional: permite ordenar por id o nombre


class LessonsListView(viewsets.ModelViewSet):
    queryset = Lessons.objects.all()
    serializer_class = LessonsSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['unit']  # Esto permite filtrar por el campo unit (id de la unidad)
    search_fields = ['name']  # Opcional: permite buscar por el nombre de la lección
    ordering_fields = ['id', 'name']  # Opcional: permite ordenar por id o nombre

class UUnitViewSet(viewsets.ModelViewSet):
    queryset = UUnit.objects.all()
    serializer_class = UUnitSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


    def create(self, request, *args, **kwargs):
        unit_id = request.data.get('unit_id')
        try:
            unit = Unit.objects.get(id=unit_id)
        except Unit.DoesNotExist:
            return Response({'error': 'Unit not found'}, status=status.HTTP_404_NOT_FOUND)
        
        uunit_data = {
            'user': request.user.id,
            'name': unit.name,
            'average': 0
        }
        serializer = self.get_serializer(data=uunit_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ULessonViewSet(viewsets.ModelViewSet):
    queryset = ULesson.objects.all()
    serializer_class = ULessonSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['unit']  # Esto permite filtrar por el campo unit (id de la unidad)
    search_fields = ['name']  # Opcional: permite buscar por el nombre de la lección
    ordering_fields = ['id', 'name']  # Opcional: permite ordenar por id o nombre

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        lesson_id = request.data.get('lesson_id')
        try:
            lesson = Lessons.objects.get(id=lesson_id)
        except Lessons.DoesNotExist:
            return Response({'error': 'Lesson not found'}, status=status.HTTP_404_NOT_FOUND)
        
        uunit, _ = UUnit.objects.get_or_create(name=lesson.unit.name)
        
        ulesson_data = {
            'user': request.user.id,
            'name': lesson.name,
            'unit': uunit.id,
            'completed': False
        }
        if(lesson.image):
            ulesson_data['image'] = lesson.image
        if(lesson.ico):
            ulesson_data['ico'] = lesson.ico
        if(lesson.video):
            ulesson_data['video'] = lesson.video
        
        serializer = self.get_serializer(data=ulesson_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        completed = request.data.get('completed', None)
        if completed is not None:
            instance.completed = completed
            instance.save()
            return Response({'status': 'completed updated'})
        return super().partial_update(request, *args, **kwargs)