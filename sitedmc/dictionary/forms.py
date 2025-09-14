from django import forms


class UploadFileForm(forms.Form):
    only_field = forms.JSONField()
