from django.contrib import admin
from .models import Task

# Register your models here.


class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'created', 'date_start', 'date_end', 'completed', 'user')

admin.site.register(Task, TaskAdmin)