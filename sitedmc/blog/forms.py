from django import forms
from .models import Blog, Tag

class AddPostForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), label='Tags for post')

    class Meta:
        model = Blog
        fields = ('title', 'content', 'is_published')
        widgets = {
            'content': forms.Textarea(attrs={'cols':50, 'rows': 5})
        }
