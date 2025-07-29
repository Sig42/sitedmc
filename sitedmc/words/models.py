from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify


class List(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    amount = models.IntegerField(default=0,  verbose_name='Количество слов')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)
    creator = models.ForeignKey(get_user_model(), related_name='list', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            s = slugify(self.name + '-' + self.creator.username)
            slug = s
            n = 1
            while List.objects.filter(slug=s).exists():
                slug = f'{s}-{n}'
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)


class Word(models.Model):
    name = models.CharField(max_length=255, verbose_name='Слово (фраза)')
    translation = models.CharField(max_length=255, verbose_name='Перевод')
    level = models.IntegerField(default=0, verbose_name='Уровень')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    update_time = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)
    list = models.ForeignKey(List, related_name='word', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            s = slugify(self.name + '-' + self.list.name)
            slug = s
            n = 1
            while Word.objects.filter(slug=s).exists():
                slug = f'{s}-{n}'
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['level']
