from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy,  reverse
from .models import Words
from django.views.generic import TemplateView, ListView, CreateView, UpdateView


class Start(LoginRequiredMixin, TemplateView):
    template_name = 'dictionary/start.html'
    first_word = Words.objects.all()[0]
    extra_context = {'current_app': 'dictionary', 'title': 'Dictionary',  'first_word': first_word}


# def learn_words(request):
#     word = Words.objects.all()[0]
#     data = {'current_app': 'dictionary', 'title': 'Dictionary',  'word': word}
#     return render(request, 'dictionary/learn_words.html', context=data)


class LearnWords(LoginRequiredMixin, UpdateView):
    model = Words
    template_name = 'dictionary/learn_words.html'
    extra_context = {'current_app': 'dictionary', 'title': 'Learning words'}
    context_object_name = 'words'
    fields = ['level']

    def get_success_url(self):
        w = Words.objects.filter(person=self.request.user)[0]
        return reverse_lazy(f'dictionary:learn_words', args=[w.pk])


class AddWords(LoginRequiredMixin, CreateView):
    template_name = 'dictionary/add_words.html'
    extra_context = {'current_app': 'dictionary', 'title': 'Adding words'}
    model = Words
    fields = ['title', 'translation']

    def get_success_url(self):
        return reverse_lazy('dictionary:show_words')

    def form_valid(self, form):
        x = form.save(commit=False)
        x.person = self.request.user
        return super().form_valid(form)


class ShowWords(ListView):
    template_name = 'dictionary/show_words.html'
    extra_context = {'current_app': 'dictionary', 'title': 'Viewing words'}
    context_object_name = 'words'

    def get_queryset(self):
        return Words.objects.filter(person=self.request.user)
