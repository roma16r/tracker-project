from django.dispatch import receiver
from django.db.models.signals import pre_save
from .models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string


@receiver(pre_save, sender=User)
def user_created(sender, instance, **kwargs):
    if instance.pk is None and instance.password == '':
        password = User.objects.make_random_password()
        instance.set_password(password)
        msg_html = render_to_string('user/emails/welcome.html', {'username': instance.username,
                                                                 'password': password})
        send_mail(
            'Welcome to tracker',
            '',
            'noreply@tracker.local',
            [instance.email],
            html_message=msg_html,
        )




