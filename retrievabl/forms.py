from django import forms
from .models import Search


class ArticleSearchForm(forms.ModelForm):
    class Meta:
        CHOICES = [('select1', 'select 1'),
                   ('select2', 'select 2')]
        model = Search
        fields = [
            'query', 'neg'
        ]
        widgets = {
            'query': forms.TextInput(attrs={'placeholder': 'Search for news'}),
            'neg': forms.RadioSelect(choices=CHOICES)
        }
