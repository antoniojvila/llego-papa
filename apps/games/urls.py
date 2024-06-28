from django.urls import path
from .views import Game1View

urlpatterns = [
    path('1/', Game1View.as_view(), name='game-1'),
]