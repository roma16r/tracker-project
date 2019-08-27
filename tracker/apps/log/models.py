from django.db import models
from tracker.apps.task.models import Task
from django.shortcuts import reverse


class Log(models.Model):
    spent_time = models.PositiveSmallIntegerField()
    comment = models.TextField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE, editable=False)

    def get_absolute_url(self):
        return reverse('logs', kwargs={'pk': self.task_id})
