from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import CreateView, UpdateView
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.urls import reverse, reverse_lazy
from .forms import UserLoginForm, UserRegistrationForm, UserProfileForm, ChangePasswordForm


def home(request):
    title = 'Главная'
    current_app = 'Home'
    return render(request, 'users/home.html', {'title': title, 'current_app': current_app})


class LoginUser(LoginView):
    form_class = UserLoginForm
    template_name = 'users/boot_login.html'
    extra_context = {'title': 'Аутентификация'}

    def get_success_url(self):
        return reverse_lazy('users:home')


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('users:login'))


class UserRegistration(CreateView):
    form_class = UserRegistrationForm
    template_name = 'users/boot_registration.html'
    extra_context = {'title': 'Регистрация'}
    success_url = reverse_lazy('users:login')


class UserProfile(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = UserProfileForm
    template_name = 'users/boot_profile.html'

    def get_success_url(self):
        return reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class ChangePassword(PasswordChangeView):
    form_class = ChangePasswordForm
    template_name = 'users/boot_password_change.html'
    success_url = reverse_lazy('users:password_change_done')
