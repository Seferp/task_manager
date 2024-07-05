from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'describe', 'date_start', 'date_end']
        label = ['Title', 'Describe', 'Start Date', 'End Date']