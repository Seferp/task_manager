from django.urls import path
from . import views
from django.contrib.auth.views import LoginView


urlpatterns = [
    path('', views.user_tasks, name='task_list'),
    path('register/', views.register_user, name='register'),
    path('register-done/', views.register_user, name='register_done'),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('create-task/', views.create_task, name='create_task'),
    path('task/<str:task_title>-<int:task_id>/', views.task_detail, name='task_detail'),
    path('task-update/<int:pk>/', views.TaskUpdate.as_view(template_name='task_manager/task_update.html'), name='task_update'),
]