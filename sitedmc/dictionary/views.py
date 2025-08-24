from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from .models import Words
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.core.exceptions import PermissionDenied


def check_auth(request):
    if request.user.is_authenticated:
        return redirect('dictionary:start')
    else:
        return redirect('dictionary:start_not_auth')


class Start(TemplateView):
    template_name = 'dictionary/start.html'
    extra_context = {'current_app': 'dictionary', 'title': 'Dictionary'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        word = Words.objects.filter(person=self.request.user)[0]
        context['word'] = word
        return context


class StartNotAuth(TemplateView):
    template_name = 'dictionary/start_not_auth.html'
    extra_context = {'current_app': 'dictionary', 'title': 'Dictionary'}


class ChooseWords(TemplateView):
    template_name = 'dictionary/choose_words.html'
    extra_context = {'current_app': 'dictionary', 'title': 'Choose words'}


class LearnWords(LoginRequiredMixin, UpdateView):
    model = Words
    template_name = 'dictionary/learn_words.html'
    extra_context = {'current_app': 'dictionary', 'title': 'Learning words'}
    context_object_name = 'words'
    fields = ['level']

    def get_success_url(self):
        w = Words.objects.filter(person=self.request.user)[0]
        return reverse_lazy('dictionary:learn_words', args=[w.pk])


class AddWords(LoginRequiredMixin, CreateView):
    template_name = 'dictionary/add_words.html'
    extra_context = {'current_app': 'dictionary', 'title': 'Adding words'}
    model = Words
    fields = ['title', 'translation']

    def get_success_url(self):
        return reverse_lazy('dictionary:add_words')

    def form_valid(self, form):
        u = self.request.user
        title = form.cleaned_data['title']
        if Words.objects.filter(title=title, person=u).exists():
            messages.error(self.request, 'У Вас уже есть такое слово в словаре!')
            return super().form_invalid(form)
        else:
            x = form.save(commit=False)
            x.person = u
            messages.success(self.request, 'Слово успешно добавлено в словарь!')
            return super().form_valid(form)


class ShowWords(LoginRequiredMixin, ListView):
    model = Words
    template_name = 'dictionary/show_words.html'
    extra_context = {'current_app': 'dictionary', 'title': 'Viewing words'}
    context_object_name = 'words'
    paginate_by = 30

    def get_queryset(self):
        pers = self.request.user
        qs = super().get_queryset().filter(person=pers)
        title = self.request.GET.get('title')
        translation = self.request.GET.get('translation')
        level = self.request.GET.get('level')
        if title:
            qs = qs.filter(title__contains=title)
        if translation:
            qs = qs.filter(translation__contains=translation)
        if level:
            qs = qs.filter(level=level)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.request.GET.get('title')
        context['translation'] = self.request.GET.get('translation')
        context['level'] = self.request.GET.get('level')
        return context


class UpdateWord(LoginRequiredMixin, UpdateView):
    model = Words
    template_name = 'dictionary/update_word.html'
    extra_context = {'current_app': 'dictionary', 'title': 'Editing word'}
    context_object_name = 'word'
    fields = ['title', 'translation', 'level']

    def get_object(self, **kwargs):
        ob = super().get_object(**kwargs)
        if ob.person == self.request.user:
            return ob
        else:
            raise PermissionDenied

    def get_success_url(self):
        return reverse_lazy('dictionary:show_words')


class DeleteWord(DeleteView):
    model = Words
    success_url = reverse_lazy('dictionary:start')
    template_name = 'dictionary/delete_word.html'
    extra_context = {'current_app': 'dictionary', 'title': 'Deleting word'}

    def get_object(self, **kwargs):
        ob = super().get_object(**kwargs)
        if ob.person == self.request.user:
            return ob
        else:
            raise PermissionDenied
