from django.shortcuts import render, HttpResponse, redirect
from django.views.generic import ListView
from .models import Task
from .forms import UserRegistrationForm
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request.Post)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('task_list')  # Przekierowanie do listy zadań po zalogowaniu
            else:
                form.add_error(None, 'Invalid username or password')
        else:
            form = AuthenticationForm()
    return render(request, 'task_manager/task_list.html', {'form': form})
def logout_view(request):
    logout(request)
    return render(request, 'task_manager/task_list.html')

def register_user(request):
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


class TaskList(ListView):
    model = Task
    context_object_name = 'task_list'
    paginate_by = 25
    ordering = ['created']
    template_name = 'task_manager/task_list.html'