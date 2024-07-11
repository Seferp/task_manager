from django.contrib import admin
from .models import Task, Comment

# Register your models here.


class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'created', 'date_start', 'date_end', 'completed', 'user')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('task', 'user', 'created', 'updated')

admin.site.register(Task, TaskAdmin)
admin.site.register(Comment, CommentAdmin)