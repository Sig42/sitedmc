from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.transaction import commit
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from .models import Blog, Tag
from.forms import AddPostForm
from django.views import View
from django.views.generic import ListView, DetailView, FormView, CreateView, UpdateView, DeleteView




class Start(ListView):
    # model = Blog
    template_name = 'blog/start.html'
    context_object_name = 'posts'
    extra_context = {'title': 'Here is start page for blog.'}
    paginate_by = 2

    def get_queryset(self):
        return Blog.published.all()


class AddPost(LoginRequiredMixin, CreateView):
    form_class = AddPostForm
    template_name = 'blog/add_post.html'
    success_url = reverse_lazy('blog:start') # Client will be directed to absolute_url, if this argument is turned off.
    extra_context = {'title': 'Add new post'}

    def form_valid(self, form):
        x = form.save(commit=False)
        x.author = self.request.user
        return super().form_valid(form)


class UpdatePost(UpdateView):
    model = Blog
    fields = ('title', 'content', 'is_published',  'tags')
    template_name = 'blog/add_post.html'
    success_url = reverse_lazy('blog:start')
    extra_context = {'title': 'Editing post'}


class DeletePost(DeleteView):
    model = Blog
    success_url = reverse_lazy('blog:start')
    template_name = 'blog/delete_post.html'


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
        return redirect('blog:start')
    post_list = Blog.objects.filter(create_time__year=year)
    paginator = Paginator(post_list, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/archive.html',
                  {'year': year, 'title': f'Archive of {year} year',
                   'page_obj': page_obj, 'paginator': paginator})


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
