from django import forms
from django.forms import TextInput, Textarea

from referendums.models import *


class ReferendumForm(forms.ModelForm):

    class Meta:
        model = Referendum
        fields = ['title', 'comment', 'top_address', ]


class QuestionForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = ['title', 'text', ]
        widgets = {
            'title': TextInput(attrs={'size': 30}),
            'text': Textarea(attrs={'rows': 4, 'cols': 50})
        }


class AnswerForm(forms.ModelForm):

    class Meta:
        model = Answer
        fields = ['label', 'comment', 'style', ]
        widgets = {
            'title': TextInput(attrs={'size': 20}),
            'comment': Textarea(attrs={'rows': 4, 'cols': 30})
        }

