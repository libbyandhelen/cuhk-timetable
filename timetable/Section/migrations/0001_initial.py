# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-01-04 18:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Course', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(max_length=12)),
                ('start', models.CharField(max_length=32)),
                ('end', models.CharField(max_length=32)),
                ('room', models.CharField(max_length=32)),
                ('meeting_dates', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section_code', models.CharField(max_length=32)),
                ('term', models.CharField(max_length=32)),
                ('type', models.CharField(max_length=32)),
                ('status', models.CharField(max_length=32)),
                ('instruction_mode', models.CharField(max_length=32)),
                ('instructor', models.CharField(max_length=32)),
                ('language', models.CharField(max_length=32)),
                ('class_capacity', models.IntegerField()),
                ('enrollment_total', models.IntegerField()),
                ('available_seat', models.IntegerField()),
                ('wait_capacity', models.IntegerField()),
                ('wait_total', models.IntegerField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Course.Course')),
            ],
        ),
        migrations.AddField(
            model_name='meeting',
            name='section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Section.Section'),
        ),
    ]