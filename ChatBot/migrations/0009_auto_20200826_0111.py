# Generated by Django 3.1 on 2020-08-25 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ChatBot', '0008_auto_20200826_0105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customers',
            name='created_by_id',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='customers',
            name='updated_by_id',
            field=models.IntegerField(null=True),
        ),
    ]
