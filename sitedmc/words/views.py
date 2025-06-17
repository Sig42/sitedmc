from django.http import HttpResponse
from django.shortcuts import render

def start(request):
    data = {'p1': 'List 1', 'p2': 'List of verbs', 'p3': 'Empty list'}
    return render(request, 'words/start.html', data)

def word_by_slug(request, word):
    return HttpResponse(f'{word}')
