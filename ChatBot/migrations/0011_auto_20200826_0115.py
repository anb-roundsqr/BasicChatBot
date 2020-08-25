# Generated by Django 3.1 on 2020-08-25 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ChatBot', '0010_auto_20200826_0114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customers',
            name='email',
            field=models.EmailField(max_length=200, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='customers',
            name='mobile',
            field=models.BigIntegerField(null=True, unique=True),
        ),
    ]
