from django.shortcuts import render, redirect, get_object_or_404
from .models import Task, Comment
from .forms import UserRegistrationForm, TaskForm, CommentForm
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST


# Create your views here.


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('task_list')
            else:
                form.add_error(None, 'Invalid username or password')
        else:
            form = AuthenticationForm()

    return render(request, 'task_manager/task_list.html', {'form': form})

def logout_view(request):
    logout(request)
    return render(request, 'task_manager/task_list.html')

def register_user(request):
    if request.user.is_authenticated:
        return redirect('task_list')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            return render(request, 'registration/register_done.html', {'new_user': new_user})
    else:
        form = UserRegistrationForm()
        return render(request, 'registration/register.html', {'form': form})

@login_required()
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            new_task.connected_users.add(request.user)
            form.save_m2m()
            return redirect('task_list')
    else:
        form = TaskForm()
        return render(request, 'task_manager/create_task.html', {'form': form})

def user_tasks(request):
    if request.user.is_authenticated:
        tasks = Task.objects.filter(user = request.user)
        return render(request, 'task_manager/task_list.html', {'tasks': tasks})

    else:
        return render(request, 'task_manager/task_list.html')

def task_detail(request, task_title, task_id):
    task = get_object_or_404(Task, title=task_title, id=task_id)
    form = CommentForm
    return render(request, 'task_manager/task_detail.html', {'task': task, 'form': form})

# @require_POST
# def task_comment(request, task_id):
#     task = get_object_or_404(Task, id=task_id)
#     comment = None
#     form = CommentForm(data=request.POST)
#     if form.is_valid():
#         comment = form.save(commit=False)
#         comment.task = task
#         comment.save()
#     return render(request, 'task_manager/task_list.html', {'task':task,
#                                                            'from': form,
#                                                            'comment': comment})
#
