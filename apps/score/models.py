from django.db import models
from django.contrib.auth import get_user_model
from datetime import timedelta

User = get_user_model()

CHOICE_GAMES = [
    (1, 'Box'),
    (2, 'Memory'),
    (3, 'Option 3'),
]

class Score(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='score', blank=True, null=True)
    score = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Socre'
        verbose_name_plural = 'Socres'

class RoundHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='round_history', blank=True, null=True)
    hits = models.IntegerField(default=0)
    errors = models.IntegerField(default=0)
    game = models.SmallIntegerField(choices=CHOICE_GAMES, default=1)
    time = models.DurationField(default=timedelta())
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return '{} - {}'.format(self.user, self.created_at)

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'RoundHistory'
        verbose_name_plural = 'RoundHistorys'