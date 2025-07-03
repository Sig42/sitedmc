from django.contrib import admin
from .models import Blog, Tag


class AuthorSpecified(admin.SimpleListFilter):
    title = 'Is an author specified?'
    parameter_name = 'is_author'

    def lookups(self, request, model_admin):
        return [
            ('yes', 'указан'),
            ('no', 'не указан')
        ]

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(author__isnull=False)
        elif self.value() == 'no':
            return queryset.filter(author__isnull=True)
        return None


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id',  'title', 'create_time', 'is_published', 'brief_info')
    list_display_links = ('id', 'title')
    list_editable = ('is_published',)
    ordering = ['-is_published', '-create_time']
    list_per_page = 5
    actions = ('make_published', 'make_draft')
    search_fields = ('title', 'tags__name')
    list_filter = ('is_published', AuthorSpecified)
    readonly_fields = ('slug', )
    filter_horizontal = ('tags', )

    @admin.display(description='Объем контента')
    def brief_info(self, blog:Blog):
        return f'Статья длиной {len(blog.content)} символов.'

    @admin.action(description='Опубликовать')
    def make_published(self, request, queryset):
        count = queryset.update(is_published=True)
        self.message_user(request, f'Опубликавано {count} статей.')

    @admin.action(description='Снять с публикации')
    def make_draft(self, request, queryset):
        count = queryset.update(is_published=False)
        self.message_user(request, f'Снято с публикации {count} записей.')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'name')
