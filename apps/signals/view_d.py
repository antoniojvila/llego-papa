from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Unit, Lessons, UserResponse
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
        return Response({'level': level}, status=status.HTTP_200_OK)

def evaluate_user_level(user):
    responses = UserResponse.objects.filter(user=user)
    unit_performance = {}

    for response in responses:
        unit_id = response.lesson.unit.id
        if unit_id not in unit_performance:
            unit_performance[unit_id] = {'correct': 0, 'total': 0, 'time': []}

        unit_performance[unit_id]['total'] += 1
        unit_performance[unit_id]['time'].append(response.time_taken)
        if response.correct:
            unit_performance[unit_id]['correct'] += 1

    lowest_performance_unit = None
    lowest_performance_score = float('inf')

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

    unit = Unit.objects.get(id=lowest_performance_unit)
    return unit.level