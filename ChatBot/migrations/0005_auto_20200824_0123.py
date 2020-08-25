# Generated by Django 3.1 on 2020-08-23 19:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ChatBot', '0004_auto_20200817_1550'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customers',
            old_name='CustomerID',
            new_name='customer_id',
        ),
        migrations.RemoveField(
            model_name='customers',
            name='email',
        ),
        migrations.AddField(
            model_name='conversation',
            name='sender',
            field=models.CharField(default='me', max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customers',
            name='created_by_id',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customers',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 24, 1, 22, 13, 837567)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customers',
            name='date_modified',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='customers',
            name='domain',
            field=models.SlugField(default='www.apollo.com', unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customers',
            name='email_id',
            field=models.EmailField(default='admin@chemstride.com', max_length=200, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customers',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='customers',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='customers',
            name='logo_path',
            field=models.TextField(default='static/images/default/org_logo.png'),
        ),
        migrations.AddField(
            model_name='customers',
            name='mobile',
            field=models.BigIntegerField(default=8888888888, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customers',
            name='org_name',
            field=models.CharField(default='Apollo', max_length=100, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customers',
            name='updated_by_id',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='customers',
            name='name',
            field=models.CharField(max_length=200),
        ),
    ]
