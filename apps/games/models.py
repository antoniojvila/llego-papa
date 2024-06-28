from django.db import models

# Create your models here.

class ItemTest(models.Model):
    signal = models.IntegerField(default=0)
    response = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'ItemTest'
        verbose_name_plural = 'ItemTests'