from django.http import HttpResponse
from django.shortcuts import render
from .models import List, Word
from django.views.generic import ListView


class Start(ListView):
    template_name = 'words/start.html'
    context_object_name = 'posts'
    extra_context = {'title': 'Words', 'current_app': 'Words'}

    def get_queryset(self):
        return List.objects.filter(creator=self.request.user.pk)


def start(request):
    l = List.objects.filter(creator=request.user)
    data = {'p1': l, 'p2': 'List of verbs', 'p3': 'Empty list', 'current_app': 'Words'}
    return render(request, 'words/start.html', data)


def word_by_slug(request, word):
    return HttpResponse(f'{word}')


def learn(request):
    if request.method == 'POST':
        pass
    else:
        words = Word.objects.all()
        return render(request,  'words/learn.html', {'words': words, 'current_app': 'Words'})


def table(request):
    words = Word.objects.all()
    return render(request, 'words/table.html', {'words': words, 'current_app': 'Words'})


def add_word(request):
    return render(request, 'words/add.html', {'current_app': 'Words'})
