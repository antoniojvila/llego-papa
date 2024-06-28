from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Signals
from .serializers.signals import SignalsSerializer

class SignalsListView(APIView):
    def get(self, request, format=None):
        signals = Signals.objects.all()
        signals_values = list(signals.values_list('value', flat=True))
        responses_meanings = list(signals.values_list('meaning', flat=True))

        custom_response = {
            "signals": signals_values,
            "responses": responses_meanings
        }

        return Response(custom_response, status=status.HTTP_200_OK)