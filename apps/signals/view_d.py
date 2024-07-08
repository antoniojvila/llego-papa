from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Unit, Lessons, UserResponse, UUnit, ULesson
from .serializers.serializers import LessonsSerializer
import random
import numpy as np
from django.db.models import Max
from numpy import mean

class DiagnosticLessonsView(APIView):
    def get(self, request):
        units = Unit.objects.all()
        lessons_data = []

        for unit in units:
            lessons = Lessons.objects.filter(unit=unit).order_by("id")[:2]

            for lesson in lessons:
                incorrect_answers = Lessons.objects.exclude(id=lesson.id).order_by("?")[
                    :5
                ]
                options = list(incorrect_answers.values("id", "name"))
                options.append({"id": lesson.id, "name": lesson.name})
                random.shuffle(options)

                lessons_data.append(
                    {"question": LessonsSerializer(lesson).data, "options": options}
                )

        return Response(lessons_data, status=status.HTTP_200_OK)

class SubmitResponseView(APIView):
    def post(self, request):
        user = request.user
        responses = request.data

        for response_data in responses:
            lesson_id = response_data.get("lesson_id")
            response = response_data.get("response")
            time_taken = response_data.get("time_taken")

            lesson = Lessons.objects.get(id=lesson_id)
            correct = response == lesson.name

            UserResponse.objects.create(
                user=user,
                lesson=lesson,
                response=response,
                correct=correct,
                time_taken=time_taken,
            )

        level = evaluate_user_level(user)
        user.level = level
        user.diagnostic_completed = True
        user.save()
        units = Unit.objects.filter(level__gte=level)
        for unit in units:
            uunit_data = {"user": request.user, "name": unit.name, "average": 0}
            uunit = UUnit.objects.create(**uunit_data)
            lessons = Lessons.objects.filter(unit=unit)
            for lesson in lessons:
                ulesson_data = {
                    "user": request.user,
                    "name": lesson.name,
                    "unit": uunit,
                    "image": lesson.image if lesson.image else None,
                    "ico": lesson.ico if lesson.ico else None,
                    "video": lesson.video if lesson.video else None,
                }
                ULesson.objects.create(**ulesson_data)
        return Response({"level": level}, status=status.HTTP_200_OK)


def evaluate_user_level(user):
    responses = UserResponse.objects.filter(user=user)
    unit_performance = {}

    # Calcula el rendimiento por unidad
    for response in responses:
        unit_id = response.lesson.unit.id
        unit_level = response.lesson.unit.level

        if unit_id not in unit_performance:
            unit_performance[unit_id] = {
                "level": unit_level,
                "correct": 0,
                "total": 0
            }

        unit_performance[unit_id]["total"] += 1
        if response.correct:
            unit_performance[unit_id]["correct"] += 1

    # Verifica si hay datos de rendimiento
    if not unit_performance:
        return 0  # Nivel por defecto si no hay respuestas

    # Calcular la precisión y el nivel ponderado
    total_correct = 0
    total_questions = 0
    weighted_levels = []

    for performance in unit_performance.values():
        total = performance["total"]
        correct = performance["correct"]
        accuracy = correct / total
        unit_level = performance["level"]

        # Pondera el nivel por la precisión
        weighted_level = accuracy * unit_level
        weighted_levels.append(weighted_level)

        total_correct += correct
        total_questions += total

    # Calcula el nivel promedio ponderado
    if weighted_levels:
        average_level = mean(weighted_levels)
    else:
        average_level = 0

    # Calcula el nivel general basado en el total de respuestas correctas e incorrectas
    overall_accuracy = total_correct / total_questions
    max_level = Unit.objects.aggregate(max_level=Max('level'))['max_level']

    final_level = round(overall_accuracy * max_level)

    return final_level

class DiagnosticResponsesView(APIView):
    def get(self, request):
        units = Unit.objects.all()
        responses_data = []

        for unit in units:
            lessons = Lessons.objects.filter(unit=unit).order_by("id")[:2]

            for lesson in lessons:
                correct_response = lesson.name

                response_data = {
                    "lesson_id": lesson.id,
                    "response": correct_response,
                    "time_taken": random.uniform(10, 30)  # Simulando un tiempo de respuesta
                }
                
                responses_data.append(response_data)

        return Response(responses_data, status=status.HTTP_200_OK)