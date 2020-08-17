# Generated by Django 2.2.7 on 2020-08-17 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ChatBot', '0003_botquestions_related'),
    ]

    operations = [
        migrations.AddField(
            model_name='bots',
            name='BotID',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='bots',
            name='bot_type',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='bots',
            name='domain',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='bots',
            name='model_name',
            field=models.CharField(max_length=125, null=True),
        ),
        migrations.AddField(
            model_name='bots',
            name='source_url',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='customers',
            name='CustomerID',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='customers',
            name='email',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
