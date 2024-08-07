from django import forms
from .models import Task, Comment
from django.contrib.auth.models import User

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'describe', 'date_start', 'date_end', 'connected_users', 'priority']

        label = {
            'title': 'Title',
            'describe': 'Describe',
            'date_start': 'Start Date',
            'date_end': 'End Date',
            'connected_users': 'Connected Users',
            'priority': 'Priority'
        }
        widgets = {
            'date_start': forms.DateInput(attrs={'type': 'date'}),
            'date_end': forms.DateInput(attrs={'type': 'date'}),
        }


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        labels = {
            'username': 'User name',
            'first_name' : 'First name',
            'last_name': 'Last name',
            'email': 'Email'
        }

        def clean_password(self):
            cd = self.cleaned_data
            if cd['password'] != cd['password2']:
                raise forms.ValidationError('Passwords don\'t macht')
            return cd['password2']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            'content': 'Comment here...'
        }