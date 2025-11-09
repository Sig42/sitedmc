from django import forms
from .models import Blog, Tag

class AddPostForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), label='Tags for post')

    class Meta:
        model = Blog
        fields = ('title', 'content', 'is_published', 'tags')
        widgets = {
            'content': forms.Textarea(attrs={'cols':50, 'rows': 5}),
        }

class TestForm(forms.Form):
    title = forms.CharField(max_length=255)
    content = forms.CharField(widget=forms.Textarea())
    is_published = forms.BooleanField()
    tags = forms.ModelChoiceField(queryset=Tag.objects.all())
