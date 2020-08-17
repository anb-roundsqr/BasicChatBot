# Generated by Django 2.2.7 on 2020-08-11 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ChatBot', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conversation',
            name='browser',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='conversation',
            name='chat_source_latitude',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='conversation',
            name='chat_source_longitude',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='conversation',
            name='time_stamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]