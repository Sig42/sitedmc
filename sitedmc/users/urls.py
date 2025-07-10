from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.urls import path
from . import views
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView

app_name = 'users'

urlpatterns = [
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('registration/', views.UserRegistration.as_view(), name='registration'),
    path('password-change/', views.ChangePassword.as_view(), name='password_change'),
    path('password-change-done/', PasswordChangeDoneView.as_view(template_name='users/password_change_done.html'),
         name='password_change_done'),
    path('profile/', views.UserProfile.as_view(), name='profile'),
]
