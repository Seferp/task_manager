from django.urls import path
from . import views
from django.contrib.auth.views import LoginView


urlpatterns = [
    path('', views.user_tasks, name='task_list'),
    path('register/', views.register_user, name='register'),
    path('register-done/', views.register_user, name='register-done'),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('create/', views.create_task, name='create'),

]