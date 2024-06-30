from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Score, RoundHistory
from .serializers.score import ScoreSerializer, RoundHistorySerializer
from rest_framework.permissions import IsAuthenticated

class ScoreListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        scores = Score.objects.filter(user=request.user)
        serializer = ScoreSerializer(scores, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class RoundHistoryCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = RoundHistorySerializer(data=request.data)
        if serializer.is_valid():
            round_history = serializer.save(user=request.user)
            score, created = Score.objects.get_or_create(user=request.user)
            score.score = score.score + round_history.hits
            score.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)