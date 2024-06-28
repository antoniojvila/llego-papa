from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

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

    def __str__(self):
        pass

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'RoundHistory'
        verbose_name_plural = 'RoundHistorys'