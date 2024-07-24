from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.urls import reverse_lazy
from .models import Task, Comment
from .forms import UserRegistrationForm, TaskForm, CommentForm
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.http import require_POST
from django.views.generic import UpdateView
from django.core.exceptions import PermissionDenied


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
        tasks = Task.objects.filter(user=request.user)
        connected_tasks = Task.objects.filter(connected_users=request.user)

        return render(request, 'task_manager/task_list.html', {
                          'tasks': tasks,
                          'connected_tasks': connected_tasks
                      })

    else:
        return render(request, 'task_manager/task_list.html')

def task_detail(request, task_title, task_id):
    task = get_object_or_404(Task, title=task_title, id=task_id)
    if task.user != request.user and request.user not in task.connected_users.all():
        raise PermissionDenied

    connected_users = task.connected_users.all()
    form = CommentForm(request.POST)
    comments = task.comments.all()

    if request.method == 'POST':
        if form.is_valid():
            comment = form.save(commit=False)
            comment.task = task
            comment.user = request.user
            comment.save()
            return redirect('task_detail',task_title=task.title, task_id=task.id)

    return render(request, 'task_manager/task_detail.html', {'task': task,
                                                             'form': form,
                                                             'comment': None,
                                                             'comments': comments,
                                                             'connected_users': connected_users})

class TaskUpdate(UpdateView):
    model = Task
    template_name = 'task_manager/task_update.html'
    fields = ['title', 'describe', 'date_start', 'date_end', 'connected_users', 'priority', 'completed']

    def get_success_url(self):
        task = self.object
        return reverse_lazy('task_detail', kwargs={'task_title': task.title, 'task_id': task.id})


