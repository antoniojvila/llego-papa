from django.urls import path
from .views import Game1View, MemoryGame1View

urlpatterns = [
    path('1/', Game1View.as_view(), name='game-1'),
    path('2/', MemoryGame1View.as_view(), name='game-1'),
]