import django.template.defaultfilters
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)


class Blog(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    slug = models.SlugField(max_length=255, unique=True)
    content = models.TextField(blank=True, verbose_name='Текст блога')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    update_time = models.DateTimeField(auto_now=True, verbose_name='Изменен')
    is_published = models.BooleanField(default=False, verbose_name='Опубликован')
    tags = models.ManyToManyField('Tag', blank=True, related_name='posts', verbose_name='Тэги')
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True,
                               related_name='posts', default=None)

    objects = models.Manager()
    published = PublishedManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self): # Чтобы иметь ссылку в шаблоне, на конкретный пост
        return reverse('show_post', kwargs={'post_slug': self.slug})

    class Meta:
        verbose_name = 'Post'
        ordering = ['-create_time']
        indexes = [models.Index(fields=['-create_time'])]


class Tag(models.Model):
    name = models.CharField(max_length=50, db_index=True, verbose_name='Имя тэга')
    slug = models.SlugField(max_length=100, db_index=True, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('posts_by_tag', kwargs={'tag_slug': self.slug})

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
