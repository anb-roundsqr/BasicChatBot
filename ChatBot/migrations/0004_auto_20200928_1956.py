# Generated by Django 3.1 on 2020-09-28 14:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ChatBot', '0003_auto_20200928_1924'),
    ]

    operations = [
        migrations.RenameField(
            model_name='admin',
            old_name='email',
            new_name='email_id',
        ),
    ]
