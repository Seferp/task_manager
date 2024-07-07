from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Task(models.Model):
    title = models.CharField(max_length=30)
    describe = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    date_start = models.DateField()
    date_end = models.DateField()
    completed = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title