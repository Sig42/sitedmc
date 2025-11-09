from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from .models import Blog, Tag
from.forms import AddPostForm, TestForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView


class Start(ListView):
    # model = Blog
    template_name = 'blog/boot_start.html'
    context_object_name = 'posts'
    extra_context = {'title': 'Последние посты пользователей:', 'current_app': 'Blog'}
    paginate_by = 3

    def get_queryset(self):
        return Blog.published.all()


class AuthorsList(ListView):
    template_name = 'blog/boot_authors.html'
    context_object_name = 'authors'
    extra_context = {'title': 'Авторы', 'current_app': 'Blog'}
    paginate_by = 3

    def get_queryset(self):
        return get_user_model().objects.all()


class TagsList(ListView):
    template_name = 'blog/boot_tags.html'
    context_object_name = 'tags'
    extra_context = {'title': 'Тэги', 'current_app': 'Blog'}
    paginate_by = 3

    def get_queryset(self):
        return Tag.objects.all()


class MyPosts(LoginRequiredMixin, ListView):
    template_name = 'blog/boot_my_posts.html'
    context_object_name = 'posts'
    extra_context = {'title': 'Мои посты', 'current_app': 'Blog'}
    paginate_by = 3
    # PermissionRequiredMixin, permission_required = 'blog.change_blog'

    def get_queryset(self):
        return Blog.objects.filter(author=self.request.user.pk)


class AddPost(LoginRequiredMixin, CreateView):
    form_class = AddPostForm
    template_name = 'blog/boot_add_post.html'
    success_url = reverse_lazy('blog:start') # Client will be directed to absolute_url, if this argument is turned off.
    extra_context = {'title': 'Добавление нового поста', 'current_app': 'Blog'}

    def form_valid(self, form):
        x = form.save(commit=False)
        x.author = self.request.user
        # x.tags.set(self.request.POST.get('tags'))
        return super().form_valid(form)


class UpdatePost(UpdateView):
    model = Blog
    fields = ('title', 'content', 'is_published',  'tags')
    template_name = 'blog/boot_add_post.html'
    success_url = reverse_lazy('blog:start')
    extra_context = {'title': 'Редактирование поста', 'current_app': 'Blog'}

    def get_object(self, **kwargs):
        ob = super().get_object(**kwargs)
        if ob.author.username == self.request.user.username:
            return ob
        else:
            raise PermissionDenied


class DeletePost(DeleteView):
    model = Blog
    success_url = reverse_lazy('blog:start')
    template_name = 'blog/boot_delete_post.html'
    extra_context = {'title': 'Удаление поста', 'current_app': 'Blog'}

    def get_object(self, **kwargs):
        ob = super().get_object(**kwargs)
        if ob.author.username == self.request.user.username:
            return ob
        else:
            raise PermissionDenied


class PostsByAuthor(ListView):
    template_name = 'blog/boot_posts_by_author.html'
    context_object_name = 'posts'
    extra_context = {'current_app': 'Blog'}
    paginate_by = 3

    def get_queryset(self):
        return Blog.published.filter(author__pk=self.kwargs['author_pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        author_pk = self.kwargs['author_pk']
        b_name = get_user_model().objects.get(pk=author_pk)
        context['blogger_name'] = b_name
        context['title'] = f'Посты пользователя {b_name}'
        return context


class ShowPost(DetailView):
    # model = Blog
    template_name = 'blog/boot_show_post.html'
    context_object_name = 'post'
    slug_url_kwarg = 'post_slug'
    extra_context = {'current_app': 'Blog'}

    def get_object(self, queryset=None):
        return  get_object_or_404(Blog.published, slug=self.kwargs[self.slug_url_kwarg])


# @permission_required(perm=permission you need, raise_exception=True) This is how permission works to function ->
# -> not classes;
def archive(request, year):
    if year > 2025:
        return redirect('blog:start')
    post_list = Blog.published.filter(create_time__year=year)
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/boot_archive.html',
                  {'year': year, 'title': f'Архив {year} года',
                   'page_obj': page_obj, 'paginator': paginator, 'current_app': 'Blog'})


def page_not_found(request, exception):
    return HttpResponseNotFound('Страница не найдена.')


class PostsByTag(ListView):
    template_name = 'blog/boot_posts_by_tag.html'
    context_object_name = 'posts'
    allow_empty = False
    extra_context = {'current_app': 'Blog'}
    paginate_by = 3

    def get_queryset(self):
        return Blog.published.filter(tags__slug=self.kwargs['tag_slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        t_name = self.kwargs['tag_slug'].capitalize()
        context['title'] = f'Посты по тэгу {t_name}'
        return context
