from django import forms
from .models import Words


class UploadFileForm(forms.Form):
    only_field = forms.JSONField()


class AddWordForm(forms.ModelForm):
    class Meta:
        model = Words
        fields = ['title', 'translation']
        labels = {
            'title': 'Слово (ин.)',
            'translation': 'Перевод (рус.)'
        }
