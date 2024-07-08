from rest_framework import generics
from .models import User
from .serializers import RegisterSerializer
from .models import User
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from apps.signals.permissions import IsProfessor
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class UserReportListView(APIView):
    permission_classes = [IsAuthenticated, IsProfessor]

    def get(self, request):
        users = User.objects.filter(role='alumno')
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['level'] = self.user.level
        data['diagnostic_completed'] = self.user.diagnostic_completed
        data['role'] = self.user.role
        return data

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
