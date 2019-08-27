from django.apps import AppConfig


class TaskConfig(AppConfig):
    name = 'tracker.apps.task'

    def ready(self):
        import tracker.apps.task.signals

