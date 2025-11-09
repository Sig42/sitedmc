import django.template.defaultfilters
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

transcription_dict = {
            'А': 'A', 'а': 'a',
            'Б': 'B', 'б': 'b',
            'В': 'V', 'в': 'v',
            'Г': 'G', 'г': 'g',
            'Д': 'D', 'д': 'd',
            'Е': 'E', 'е': 'e',
            'Ё': 'Yo', 'ё': 'yo',
            'Ж': 'Zh', 'ж': 'zh',
            'З': 'Z', 'з': 'z',
            'И': 'I', 'и': 'i',
            'Й': 'Y', 'й': 'y',
            'К': 'K', 'к': 'k',
            'Л': 'L', 'л': 'l',
            'М': 'M', 'м': 'm',
            'Н': 'N', 'н': 'n',
            'О': 'O', 'о': 'o',
            'П': 'P', 'п': 'p',
            'Р': 'R', 'р': 'r',
            'С': 'S', 'с': 's',
            'Т': 'T', 'т': 't',
            'У': 'U', 'у': 'u',
            'Ф': 'F', 'ф': 'f',
            'Х': 'Kh', 'х': 'kh',
            'Ц': 'Ts', 'ц': 'ts',
            'Ч': 'Ch', 'ч': 'ch',
            'Ш': 'Sh', 'ш': 'sh',
            'Щ': 'Shch', 'щ': 'shch',
            'Ъ': '', 'ъ': '',  # твердый знак обычно не транскрибируется
            'Ы': 'Y', 'ы': 'y',
            'Ь': '', 'ь': '',  # мягкий знак обычно не транскрибируется
            'Э': 'E', 'э': 'e',
            'Ю': 'Yu', 'ю': 'yu',
            'Я': 'Ya', 'я': 'ya'
        }


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
        return reverse('blog:show_post', kwargs={'post_slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            result_list = []
            for char in self.title:
                if char in transcription_dict:
                    result_list.append(transcription_dict[char])
                else:
                    result_list.append(char)
            result_str = ''.join(result_list)
            s = slugify(result_str)
            n = 1
            slug = s
            while Blog.objects.filter(slug=slug).exists():
                slug = f'{s}-{n}'
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)

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
        return reverse('blog:posts_by_tag', kwargs={'tag_slug': self.slug})

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
