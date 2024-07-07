from django import forms
from .models import Task
from django.contrib.auth.models import User

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'describe', 'date_start', 'date_end']
        label = ['Title', 'Describe', 'Start Date', 'End Date']

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Passowrd', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email',]
        label = ['Username', 'First name', 'Last name', 'Email',]

        def clean_password(self):
            cd = self.cleaned_data
            if cd['password'] != cd['password2']:
                raise forms.ValidationError('Passwords don\'t macht')
            return cd['password2']