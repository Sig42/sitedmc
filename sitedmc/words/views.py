from django.http import HttpResponse
from django.shortcuts import render
from .models import List, Word
from django.views.generic import ListView, CreateView, UpdateView, TemplateView


class Start(TemplateView):
    template_name = 'words/start.html'
    extra_context = {'title': 'Words', 'current_app': 'Words'}


class CreateList(CreateView):
    model = List
    template_name = 'words/create_list.html'
    extra_context = {'title': 'Creating new list', 'current_app': 'Words'}
    fields = ['name']

    def form_valid(self, form):
        x = form.save(commit=False)
        x.creator = self.request.user
        return super().form_valid(form)


class MyLists(ListView):
    pass


class AddWords(UpdateView):
    pass


class LearnWords(ListView):
    pass


class ShowList(ListView):
    pass


#
# def word_by_slug(request, word):
#     return HttpResponse(f'{word}')
#
#
# def learn(request):
#     if request.method == 'POST':
#         pass
#     else:
#         words = Word.objects.all()
#         return render(request,  'words/learn.html', {'words': words, 'current_app': 'Words'})
#
#
# def table(request):
#     words = Word.objects.all()
#     return render(request, 'words/table.html', {'words': words, 'current_app': 'Words'})
#
#
# def add_word(request):
#     return render(request, 'words/add.html', {'current_app': 'Words'})
