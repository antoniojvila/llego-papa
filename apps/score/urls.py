from django.urls import path
from .views import ScoreListView, RoundHistoryCreateView

urlpatterns = [
    path('scores/', ScoreListView.as_view(), name='score_list'),
    path('round-history/', RoundHistoryCreateView.as_view(), name='round_history_create'),
]