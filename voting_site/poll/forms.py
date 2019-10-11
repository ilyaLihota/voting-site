from datetime import date
from django import forms
from poll.models import *
from django.core.exceptions import ValidationError


class PollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = [
            'title',
            'description',
            'start_at',
            'end_at',
            'amount_of_questions',
            'picture',
        ]

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'start_at': forms.DateInput(format=('%d-%m-%Y %H:%M'), attrs={'type': 'datetime-local', 'localize': True}),
            'end_at': forms.DateInput(format=('%d-%m-%Y %H:%M'), attrs={'type': 'datetime-local', 'localize': True}),
            'amount_of_questions': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def clean_title(self):
        new_title = self.cleaned_data['title'].lower()

        if Poll.objects.filter(title__iexact=new_title).count():
            raise ValidationError('Title must be unique. We have "{}" title already'.format(new_title))
        return new_title


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
        }
