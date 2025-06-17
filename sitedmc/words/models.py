from django.db import models
from django.contrib.auth.models import User


class List(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    amount = models.IntegerField(default=0,  verbose_name='Количество слов')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    creator = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)


class Word(models.Model):
    name = models.CharField(max_length=255, verbose_name='Слово (фраза)')
    translation = models.CharField(max_length=255, verbose_name='Перевод')
    level = models.IntegerField(default=0, verbose_name='Уровень')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    update_time = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
    list = models.ForeignKey(List, related_name='list', on_delete=models.CASCADE)

