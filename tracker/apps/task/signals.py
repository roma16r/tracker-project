from django.dispatch import receiver
from django.db.models.signals import pre_save
from .models import Task
from django.db.models.fields import Field
from django.core.mail import send_mail
from django.template.loader import render_to_string


@receiver(pre_save, sender=Task)
def task_changed(sender, instance, **kwargs):
    if instance.pk is None:
        return
    old_instance = sender.objects.get(pk=instance.pk)
    fields = sender._meta.get_fields()
    changed_fields = []

    for field in fields:
        if isinstance(field, Field):
            old_field = getattr(old_instance, field.name)
            new_field = getattr(instance, field.name)
            if old_field != new_field:
                changed_fields.append((field.verbose_name.capitalize(), field_formatter(field.name, old_field),
                                       field_formatter(field.name, new_field)))

    recipient_list = [instance.creator.email, instance.executor.email]
    msg_html = render_to_string('task/emails/changed_fields.html', {'changed_fields': changed_fields})

    if changed_fields:
        send_mail(
            'Task has been changed',
            '',
            'noreply@tracker.local',
            recipient_list,
            html_message=msg_html,
        )


def field_formatter(field_name, val):
    if field_name == 'type':
        return [el[1] for el in Task.TYPE_CHOICES if el[0] == val][0]
    if field_name == 'priority':
        return [el[1] for el in Task.PRIORITY_CHOICES if el[0] == val][0]
    return val

