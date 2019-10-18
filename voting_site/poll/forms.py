from datetime import date
from django import forms
from poll.models import *
from django.core.exceptions import ValidationError

from .models import *


class PollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = [
            'title',
            'description',
            'start_at',
            'end_at',
            'picture',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'start_at': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_at': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'picture': forms.FileInput(attrs={'type': 'file', 'id': 'id_picture'})
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


class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['title']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
        }
