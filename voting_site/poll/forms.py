from datetime import date
from django import forms
from poll.models import *
from django.core.exceptions import ValidationError

from .models import *
from django.forms.models import inlineformset_factory, BaseInlineFormSet

from django.contrib.admin.widgets import AdminDateWidget


class BaseQuestionFormset(BaseInlineFormSet):

    def add_fields(self, form, index):
        super(BaseQuestionFormset, self).add_fields(form, index)

        # save the formset in the 'nested' property
        form.nested = ChoiceFormset(
            instance=form.instance,
            data=form.data if form.is_bound else None,
            files=form.files if form.is_bound else None,
            prefix='choice-{}-{}'.format(
                form.prefix,
                ChoiceFormset.get_default_prefix()),
            # extra=1
        )

    def is_valid(self):
        result = super(BaseQuestionFormset, self).is_valid()

        if self.is_bound:
            for form in self.forms:
                if hasattr(form, 'nested'):
                    result = result and form.nested.is_valid()
        return result

    def save(self, commit=True):
        result = super(BaseQuestionFormset, self).save(commit=commit)

        for form in self.forms:
            if hasattr(form, 'nested'):
                if not self._should_delete_form(form):
                    form.nested.save(commit=commit)
        return result


QuestionFormset = inlineformset_factory(
        Poll,
        Question,
        formset=BaseQuestionFormset,
        extra=1,
        fields='__all__'
    )

ChoiceFormset = inlineformset_factory(
        Question,
        Choice,
        extra=1,
        fields='__all__'
    )


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
            'start_at': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_at': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            # 'end_at': forms.SelectDateWidget(),
            # 'start_at': forms.SelectDateWidget(),
            # 'end_at': forms.DateInput(format=('%d-%m-%Y %H:%M'), attrs={'type': 'datetime-local', 'localize': True}),
            'amount_of_questions': forms.NumberInput(attrs={'class': 'form-control'}),
            'picture': forms.FileInput(attrs={'type': 'file'})
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
