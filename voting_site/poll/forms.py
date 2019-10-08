from django import forms
from poll.models import *
from django.core.exceptions import ValidationError


class MySplitDateTimeWidget(forms.SplitDateTimeWidget):
    def init(self, date_format='%d-%m-%d', time_format='%H:%M:%S'):
        date_class = attrs.pop('date_class')
        time_class = attrs.pop('time_class')

        widgets = (
            DateInput(attrs={'class' : date_class}, format=date_format),
            TimeInput(attrs={'class' : time_class}, format=time_format)
        )
        # super(SplitDateTimeWidget, self).init(widgets, attrs)

class PollForm(forms.ModelForm):
    start_at = forms.SplitDateTimeField(widget=MySplitDateTimeWidget)
    end_at = forms.SplitDateTimeField(widget=MySplitDateTimeWidget)
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
            'my_date_time_field': MySplitDateTimeWidget(),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            # 'start_at': forms.DateTimeInput(),
            # 'end_at': forms.DateTimeInput(),
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
