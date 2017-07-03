from django import forms
from StudentPoll.models import Faculty, Group, Subject, Vote, Category
from django.contrib.auth.models import User
import datetime


class SelectVoteForm(forms.Form):
    vote = forms.ModelChoiceField(
        queryset=Vote.objects.all().order_by('faculty__facultyName', 'startYear').filter(isActive=1),
        label='Опитування')
    course = forms.ChoiceField(choices=(('---------','---------'),(1,1),(2,2),(3,3),(4,4)), label='Курс')
    group = forms.ModelChoiceField(queryset=Group.objects.none(), label='Напрям')


class LoginForm(forms.Form):
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Login'}))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))


class PollAdd(forms.Form):
    faculty = forms.ModelChoiceField(queryset=Faculty.objects.all(), label='Факультет')
    year = forms.ChoiceField(choices=[('{}/{}'.format(x, x+1),'{}/{}'.format(x, x+1))
                                           for x in range (datetime.datetime.now().year-3, datetime.datetime.now().year+1)],
                                  label='Навчальноко рік')
    half = forms.ChoiceField(choices=((1, '1'),(2, '2')), label='Семестр')
    categories = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), label='Категорії оцінювання')
    isActive = forms.BooleanField(label='Активувати', required=False)


class EditState(forms.Form):
    vote = forms.ModelChoiceField(queryset=Vote.objects.all(), label='Опитування')
    activate = forms.ChoiceField(widget=forms.RadioSelect, choices=((True, 'Активувати'),(False, 'Деактивувати')),
                                 label='Стан опитування', required=True)


class SelectStatisticsVoteForm(forms.Form):
    vote = forms.ModelChoiceField(
        queryset=Vote.objects.all().order_by('faculty__facultyName', 'startYear').filter(isActive=0),
        label='Опитування')