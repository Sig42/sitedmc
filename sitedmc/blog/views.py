from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from .models import Blog, Tag
from.forms import AddPostForm
from django.views import View
from django.views.generic import ListView


class Start(ListView):
    # model = Blog
    template_name = 'blog/start.html'
    context_object_name = 'posts'
    extra_context = {'title': 'Here is start page for blog.'}

    def get_queryset(self):
        return Blog.published.all()


class AddPost(View):
    def post(self, request):
        form = AddPostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('start')
        data = {
            'title': 'Adding post',
            'form': form
        }
        return render(request, 'blog/add_post.html', data)

    def get(self, request):
        form = AddPostForm()
        data = {
            'title': 'Adding post',
            'form': form
        }
        return render(request, 'blog/add_post.html', data)


# class PostsByName(ListView): !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


def posts_by_name(request, blogger_name):
    return render(request, 'blog/posts_by_name.html',
                  {'blogger_name': blogger_name, 'title': f"{blogger_name}'s posts"})


def archive(request, year):
    if year > 2025:
        return redirect('start')
    return render(request, 'blog/archive.html', {'year': year, 'title': f'Archive of {year} year'})


def page_not_found(request, exception):
    return HttpResponseNotFound('Страница не найдена.')


def show_post(request, post_slug):
    post = get_object_or_404(Blog, slug=post_slug)
    data = {
        'title': post.title,
        'content': post.content,
        'created': post.create_time
    }
    return render(request, 'blog/show_post.html', data)


class PostsByTag(ListView):
    template_name = 'blog/posts_by_tag.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Blog.published.filter(tags__slug=self.kwargs['tag_slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        t_name = self.kwargs['tag_slug'].capitalize()
        context['tag_name'] = t_name
        context['title'] = f'Posts by tag {t_name}'
        return context
