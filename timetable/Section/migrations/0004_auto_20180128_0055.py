# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-01-28 00:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Section', '0003_selectsection'),
    ]

    operations = [
        migrations.AddField(
            model_name='selectsection',
            name='bgcolor',
            field=models.CharField(default='', max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='selectsection',
            name='color',
            field=models.CharField(default='', max_length=10, null=True),
        ),
    ]
