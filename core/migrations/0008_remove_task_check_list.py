# Generated by Django 5.2.3 on 2025-07-06 19:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_task_check_list'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='check_list',
        ),
    ]
