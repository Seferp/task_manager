from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Task(models.Model):
    title = models.CharField(max_length=30)
    describe = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    date_start = models.DateField(blank=True, null=True)
    date_end = models.DateField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_task')
    connected_users = models.ManyToManyField(User, related_name='connected_users', blank=True)
    priority = models.CharField(choices=[('Low priority', 'Low priority'),
                                         ('Medium priority', 'Medium priority'),
                                         ('High priority', 'High priority')], default='Low priority')
    def __str__(self):
        return self.title

    def clean(self):
        if self.date_end and self.date_start:
            if self.date_end < self.date_start:
                self.date_start = self.date_end

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)