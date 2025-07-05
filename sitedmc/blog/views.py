from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy

from .models import Blog, Tag
from.forms import AddPostForm
from django.views import View
from django.views.generic import ListView, DetailView,FormView


class Start(ListView):
    # model = Blog
    template_name = 'blog/start.html'
    context_object_name = 'posts'
    extra_context = {'title': 'Here is start page for blog.'}

    def get_queryset(self):
        return Blog.published.all()


class AddPost(FormView):
    form_class = AddPostForm
    template_name = 'blog/add_post.html'
    success_url = reverse_lazy('start')
    extra_context = {'title': 'Add new post'}

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class PostsByName(ListView):
    template_name = 'blog/posts_by_name.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Blog.published.filter(author__username=self.kwargs['blogger_name'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        b_name = self.kwargs['blogger_name'].capitalize()
        context['blogger_name'] = b_name
        context['title'] = f'Here are posts of {b_name}'
        return context


class ShowPost(DetailView):
    # model = Blog
    template_name = 'blog/show_post.html'
    context_object_name = 'post'
    slug_url_kwarg = 'post_slug'

    def get_object(self, queryset=None):
        return  get_object_or_404(Blog.published, slug=self.kwargs[self.slug_url_kwarg])


def archive(request, year):
    if year > 2025:
        return redirect('start')
    return render(request, 'blog/archive.html', {'year': year, 'title': f'Archive of {year} year'})


def page_not_found(request, exception):
    return HttpResponseNotFound('Страница не найдена.')


class PostsByTag(ListView):
    template_name = 'blog/posts_by_tag.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Blog.published.filter(tags__slug=self.kwargs['tag_slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        t_name = self.kwargs['tag_slug'].capitalize()
        context['title'] = f'Posts by tag {t_name}'
        return context
