# Generated by Django 2.2.7 on 2020-08-10 08:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ChatBot', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clientquestions',
            name='created_by_id',
        ),
        migrations.RemoveField(
            model_name='clientquestions',
            name='updated_by_id',
        ),
    ]
