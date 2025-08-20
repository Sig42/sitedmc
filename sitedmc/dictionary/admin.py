from django.contrib import admin
from .models import Words

@admin.register(Words)
class WordsAdmin(admin.ModelAdmin):
    list_display = ('title', 'translation', 'level', 'create_time', 'person')
    list_display_links = ('title', )
    ordering = ('level', 'create_time')
