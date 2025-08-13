from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy,  reverse
from .models import Words
from django.views.generic import TemplateView, ListView, CreateView, UpdateView


class Start(TemplateView):
    template_name = 'dictionary/start.html'
    first_word = Words.objects.all()[0]
    extra_context = {'current_app': 'dictionary', 'title': 'Dictionary',  'first_word': first_word}


class LearnWords(LoginRequiredMixin, UpdateView):
    model = Words
    template_name = 'dictionary/learn_words.html'
    extra_context = {'current_app': 'dictionary', 'title': 'Learning words'}
    context_object_name = 'words'
    fields = ['level']

    def get_success_url(self):
        w = Words.objects.filter(person=self.request.user)[0]
        return reverse_lazy('dictionary:learn_words', args=[w.pk])
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

class AddWords(LoginRequiredMixin, CreateView):
    template_name = 'dictionary/add_words.html'
    extra_context = {'current_app': 'dictionary', 'title': 'Adding words'}
    model = Words
    fields = ['title', 'translation']

    def get_success_url(self):
        return reverse_lazy('dictionary:add_words')

    def form_valid(self, form):
        x = form.save(commit=False)
        x.person = self.request.user
        return super().form_valid(form)


class ShowWords(LoginRequiredMixin, ListView):
    template_name = 'dictionary/show_words.html'
    extra_context = {'current_app': 'dictionary', 'title': 'Viewing words'}
    context_object_name = 'words'

    def get_queryset(self):
        return Words.objects.filter(person=self.request.user)
