from django.http import HttpResponse
from django.shortcuts import render
from .models import List, Word

def start(request):
    l = List.objects.get(pk=1)
    data = {'p1': l, 'p2': 'List of verbs', 'p3': 'Empty list'}
    return render(request, 'words/start.html', data)

def word_by_slug(request, word):
    return HttpResponse(f'{word}')


def learn(request):
    return render(request,  'words/learn.html')


def table(request):
    words = Word.objects.all()
    return render(request, 'words/table.html', {'words': words})


def add_word(request):
    return render(request, 'words/add.html')
