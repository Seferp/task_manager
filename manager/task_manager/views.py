from django.shortcuts import render, redirect
from .models import Task
from .forms import UserRegistrationForm, TaskForm
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import AuthenticationForm


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

def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
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

