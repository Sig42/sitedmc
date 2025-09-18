from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from .forms import UploadFileForm
from .models import Words
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView, FormView
from django.core.exceptions import PermissionDenied
import json


# Поскольку слова привязаны к пользователю, проверяю зарегистрирован ли пользователь.
def check_auth(request):
    if request.user.is_authenticated:
        return redirect('dictionary:start')
    else:
        return redirect('dictionary:start_not_auth')


# Проверяю есть ли у пользователя хотя бы одно слово в списке.
# Если нет - ему будет доступна только кнопка add, добавляющая слова.
# Если уже есть слова - доступен полный функционал.
class Start(TemplateView):
    template_name = 'dictionary/start.html'
    extra_context = {'current_app': 'dictionary', 'title': 'Dictionary'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_list'] = Words.objects.filter(person=self.request.user).exists()
        return context


# View для незарегистрированного пользователя.
# Вместо кнопок стандартного функционала - кнопки log in / registrate.
class StartNotAuth(TemplateView):
    template_name = 'dictionary/start_not_auth.html'
    extra_context = {'current_app': 'dictionary', 'title': 'Dictionary'}


# Это был первый вариант работы приложения.
# Get-запрос - получаем одно слово, post-запрос - изменяем поле level в соответствии с результатом.
# С практической точки зрения оказалось неудобно.
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
        context['count'] = self.get_queryset().count()
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


# Уточняю у пользователя информацию о количестве слов и их уровне (поле level).
# Затем передаю эту информацию в функцию learn_list через url.
def pre_learn(request):
    choices = list(Words.objects.values_list('level', flat=True).distinct())
    choices.append('All')
    context = {'current_app': 'dictionary', 'title': "Choosing words", 'choices': choices}
    return render(request, 'dictionary/pre_learn.html', context=context)


def learn_list(request):
    lvl = request.GET.get('level')
    qnt = int(request.GET.get('quantity'))
    pers = request.user
    if request.method == 'POST':
        json_form = request.POST['only_field']
        words = json.loads(json_form)
        for word in words:
            w = Words.objects.get(pk=word['pk'])
            w.level = word['level']
            w.save()
        return redirect('dictionary:start')
    else:
        if lvl == 'All':
            ws = Words.objects.filter(person=pers)[:qnt]
        else:
            ws = Words.objects.filter(level=int(lvl), person=pers)[:qnt]
        # Здесь создаю словарь для последующей сериализации.
        # Можно сериализовать через встроенный инструмент Джанго, но так я получу только нужные поля
        # и не буду передавать лишние байты по сети.
        data = []
        for w in ws:
            data.append({'pk':w.pk, 'title': w.title, 'translation': w.translation, 'level': w.level})
        # Переворачиваю, потому что порядок выдачи важен - сначала слова с наименьшим полем level.
        data = data[::-1]
        json_data = json.dumps(data)
        form = UploadFileForm()
    return render(request, 'dictionary/learn_list.html',
                 {'words': json_data,
                         'form': form,
                         'title': 'Learning words',
                         'current_app': 'dictionary'})
