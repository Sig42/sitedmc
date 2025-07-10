from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Name')
    password = forms.CharField(label='Password', widget=forms.PasswordInput())

    class Meta:
        model = get_user_model()
        fields = ('username', 'password')


class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(label='Name')
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Check password', widget=forms.PasswordInput())

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
        labels = {
            'email': 'E-mail',
            'last_name': 'Last name',
            'first_name': 'First name'
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError('Such email already exists!')
        return email


class UserProfileForm(forms.ModelForm):
    username = forms.CharField(disabled=True,  label='Username', widget=forms.TextInput())
    email = forms.CharField(disabled=True,  label='E-mail', widget=forms.TextInput())

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name')
        labels = {
            'last_name': 'Last name',
            'first_name': 'First name'
        }
        widgets = {
            'first_name': forms.TextInput(),
            'last_name': forms.TextInput()
        }


class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(label='Old password', widget=forms.PasswordInput())
    new_password1 = forms.CharField(label='New password', widget=forms.PasswordInput())
    new_password2 = forms.CharField(label='Confirm new password', widget=forms.PasswordInput())
