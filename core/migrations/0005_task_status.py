# Generated by Django 5.2.3 on 2025-07-06 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_task_assigned_to'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='status',
            field=models.CharField(blank=True, choices=[('pending', 'Pending'), ('in progress', 'In Progress'), ('completed', 'Completed')], default='pending', max_length=20, null=True),
        ),
    ]
