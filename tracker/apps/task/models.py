from django.db import models
from django.conf import settings
from django.utils import timezone
from django.shortcuts import reverse
from tracker.apps.project.models import Project


class Comment(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    task = models.ForeignKey('Task', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.text


class Task(models.Model):
    FEATURE = 0
    BUG = 1

    NORMAL = 0
    HIGH = 1
    LOW = 2

    TYPE_CHOICES = [
        (FEATURE, 'Feature'),
        (BUG, 'Bug')
    ]

    PRIORITY_CHOICES = [
        (NORMAL, 'Normal'),
        (HIGH, 'High'),
        (LOW, 'Low')
    ]

    topic = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    finish_date = models.DateField()
    type = models.PositiveSmallIntegerField(choices=TYPE_CHOICES)
    priority = models.PositiveSmallIntegerField(choices=PRIORITY_CHOICES)
    estimate_time = models.PositiveSmallIntegerField()
    executor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tasks_executor')
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, editable=False,
                                related_name='tasks_creator')
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return self.topic

    def get_absolute_url(self):
        return reverse('task-detail', kwargs={'pk': self.pk})
