from django.db import models

# Create your models here.

class Signals(models.Model):
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=50)
    meaning = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Signals'
        verbose_name_plural = 'Signalss'