from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.paginator import Paginator
from django.db.transaction import commit
from django.http import HttpResponseNotFound, HttpResponse
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
    extra_context = {'title': 'Blog', 'current_app': 'Blog'}
    paginate_by = 3

    def get_queryset(self):
        return Blog.published.all()


class AuthorsList(ListView):
    template_name = 'blog/authors.html'
    context_object_name = 'authors'
    extra_context = {'title': 'Blog', 'current_app': 'Blog'}
    paginate_by = 3

    def get_queryset(self):
        return get_user_model().objects.all()


class AddPost(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    form_class = AddPostForm
    template_name = 'blog/add_post.html'
    success_url = reverse_lazy('blog:start') # Client will be directed to absolute_url, if this argument is turned off.
    extra_context = {'title': 'Add new post', 'current_app': 'Blog'}
    permission_required = 'blog.add_blog'

    def form_valid(self, form):
        x = form.save(commit=False)
        x.author = self.request.user
        return super().form_valid(form)


class UpdatePost(UpdateView):
    model = Blog
    fields = ('title', 'content', 'is_published',  'tags')
    template_name = 'blog/add_post.html'
    success_url = reverse_lazy('blog:start')
    extra_context = {'title': 'Editing post', 'current_app': 'Blog'}


class DeletePost(DeleteView):
    model = Blog
    success_url = reverse_lazy('blog:start')
    template_name = 'blog/delete_post.html'
    extra_context = {'current_app': 'Blog'}


class PostsByName(ListView):
    template_name = 'blog/posts_by_name.html'
    context_object_name = 'posts'
    extra_context = {'current_app': 'Blog'}
    paginate_by = 3

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
    return render(request, 'blog/archive.html',
                  {'year': year, 'title': f'Archive of {year} year',
                   'page_obj': page_obj, 'paginator': paginator, 'current_app': 'Blog'})


def page_not_found(request, exception):
    return HttpResponseNotFound('Страница не найдена.')


class PostsByTag(ListView):
    template_name = 'blog/posts_by_tag.html'
    context_object_name = 'posts'
    allow_empty = False
    extra_context = {'current_app': 'Blog'}
    paginate_by = 3

    def get_queryset(self):
        return Blog.published.filter(tags__slug=self.kwargs['tag_slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        t_name = self.kwargs['tag_slug'].capitalize()
        context['title'] = f'Posts by tag {t_name}'
        return context


# def get_some(request, pk): It's a draft for restricting by authorship.
#     user_name = request.user.username
#     post = Blog.objects.get(pk=pk)
#     if post.author.username == user_name:
#         return HttpResponse("You got it!")
#     return HttpResponse('You are not allowed!')
