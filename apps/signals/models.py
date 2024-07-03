from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Unit(models.Model):
    name = models.CharField(max_length=20)
    level = models.IntegerField(default=0)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Unit'
        verbose_name_plural = 'Units'
        ordering = ['level']
    
    def __str__(self) -> str:
        return '{} - {}'.format(self.level, self.name)

class Lessons(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    ico = models.ImageField(upload_to='images/', blank=True, null=True)
    video = models.FileField(upload_to='videos/', blank=True, null=True)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)   

    class Meta:
        verbose_name = 'Lessons'
        verbose_name_plural = 'Lessons'

    def __str__(self) -> str:
        return self.name
class UUnit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_unit')
    name = models.CharField(max_length=20)
    average = models.IntegerField(default=0)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)


class ULesson(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_lesson')
    name = models.CharField(max_length=20)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    ico = models.ImageField(upload_to='images/', blank=True, null=True)
    video = models.FileField(upload_to='videos/', blank=True, null=True)
    unit = models.ForeignKey(UUnit, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

class UserResponse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lessons, on_delete=models.CASCADE)
    response = models.CharField(max_length=100)
    correct = models.BooleanField(default=False)
    time_taken = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)