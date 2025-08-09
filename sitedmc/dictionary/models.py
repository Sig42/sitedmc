from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify


class Words(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    translation = models.CharField(max_length=255, verbose_name='Перевод')
    level = models.IntegerField(default=0, verbose_name='Уровень')
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)
    create_time = models.DateField(auto_now_add=True, verbose_name='Создан')
    update_time = models.DateField(auto_now=True, verbose_name='Изменен')
    person = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True,
                               related_name='ws', default=None)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['level']
