# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-07 19:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SMSLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=30)),
                ('phone', models.CharField(max_length=11)),
                ('status_code', models.IntegerField(null=True)),
                ('error_msg', models.CharField(max_length=255, null=True)),
            ],
        ),
    ]
