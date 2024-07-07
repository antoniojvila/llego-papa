from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Unit, Lessons, UserResponse, UUnit, ULesson
from .serializers.serializers import LessonsSerializer
import random
import numpy as np

class DiagnosticLessonsView(APIView):
    def get(self, request):
        units = Unit.objects.all()
        lessons_data = []

        for unit in units:
            lessons = Lessons.objects.filter(unit=unit).order_by('?')[:2]

            for lesson in lessons:
                incorrect_answers = Lessons.objects.exclude(id=lesson.id).order_by('?')[:5]
                options = list(incorrect_answers.values('id', 'name'))
                options.append({'id': lesson.id, 'name': lesson.name})
                random.shuffle(options)

                lessons_data.append({
                    'question': LessonsSerializer(lesson).data,
                    'options': options
                })

        return Response(lessons_data, status=status.HTTP_200_OK)

class SubmitResponseView(APIView):
    def post(self, request):
        user = request.user
        responses = request.data

        for response_data in responses:
            lesson_id = response_data.get('lesson_id')
            response = response_data.get('response')
            time_taken = response_data.get('time_taken')

            lesson = Lessons.objects.get(id=lesson_id)
            
            correct = (response == lesson.name)

            UserResponse.objects.create(
                user=user,
                lesson=lesson,
                response=response,
                correct=correct,
                time_taken=time_taken
            )

        level = evaluate_user_level(user)
        user.level = level
        user.save()
        units = Unit.objects.filter(level__gte=level)
        for unit in units:
            uunit_data = {
                'user': request.user,
                'name': unit.name,
                'average': 0
            }
            uunit = UUnit.objects.create(**uunit_data)
            lessons = Lessons.objects.filter(unit=unit)
            for lesson in lessons:
                ulesson_data = {
                    'user': request.user,
                    'name': lesson.name,
                    'unit': uunit,
                    'image': lesson.image.url if lesson.image else None,
                    'ico': lesson.image.url if lesson.ico else None,
                    'video': lesson.video.url if lesson.video else None
                }
                ULesson.objects.create(**ulesson_data)
        return Response({'level': level}, status=status.HTTP_200_OK)

def evaluate_user_level(user):
    responses = UserResponse.objects.filter(user=user)
    unit_performance = {}

    # Calcula el rendimiento por unidad
    for response in responses:
        unit_id = response.lesson.unit.id
        if unit_id not in unit_performance:
            unit_performance[unit_id] = {'correct': 0, 'total': 0, 'time': []}

        unit_performance[unit_id]['total'] += 1
        unit_performance[unit_id]['time'].append(response.time_taken)
        if response.correct:
            unit_performance[unit_id]['correct'] += 1

    # Verifica si hay datos de rendimiento
    if not unit_performance:
        return 0  # O algún valor por defecto que indique el nivel del usuario

    lowest_performance_unit = None
    lowest_performance_score = float('inf')

    # Encuentra la unidad con el peor rendimiento
    for unit_id, performance in unit_performance.items():
        correct = performance['correct']
        total = performance['total']
        avg_time = np.mean(performance['time'])
        stddev_time = np.std(performance['time'])

        accuracy = correct / total
        avg_time_penalty = np.mean([time - avg_time for time in performance['time'] if time > avg_time])

        performance_score = (1 - accuracy) + avg_time_penalty

        if performance_score < lowest_performance_score:
            lowest_performance_score = performance_score
            lowest_performance_unit = unit_id

    # Verifica si lowest_performance_unit ha sido actualizado
    if lowest_performance_unit is None:
        return 0  # O algún valor por defecto que indique el nivel del usuario

    try:
        unit = Unit.objects.get(id=lowest_performance_unit)
    except Unit.DoesNotExist:
        return 0  # O algún valor por defecto que indique el nivel del usuario

    return unit.level
