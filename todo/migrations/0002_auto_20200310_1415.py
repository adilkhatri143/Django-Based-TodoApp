# Generated by Django 3.0.3 on 2020-03-10 14:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='todo',
            old_name='date_completed',
            new_name='datecompleted',
        ),
    ]