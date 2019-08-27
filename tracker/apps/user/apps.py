from django.apps import AppConfig


class UserConfig(AppConfig):
    name = 'tracker.apps.user'

    def ready(self):
        import tracker.apps.user.signals
