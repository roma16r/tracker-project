# Generated by Django 2.2.4 on 2019-08-12 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('log', '0002_log_task'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='comment',
            field=models.TextField(),
        ),
    ]
