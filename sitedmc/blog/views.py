from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect


def start(request):
    return render(request, 'blog/start.html')


def add_post(request):
    pass


def posts_by_name(request, blogger_name):
    return render(request, 'blog/posts_by_name.html', {'blogger_name': blogger_name})


def archive(request, year):
    if year > 2025:
        return redirect('start')
    return render(request, 'blog/archive.html', {"year": year})


def page_not_found(request, exception):
    return HttpResponseNotFound('Страница не найдена.')
