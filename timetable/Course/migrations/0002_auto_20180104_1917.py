# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-01-04 19:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Course', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='add_consent',
            field=models.CharField(default='', max_length=32),
        ),
        migrations.AlterField(
            model_name='course',
            name='career',
            field=models.CharField(default='', max_length=32),
        ),
        migrations.AlterField(
            model_name='course',
            name='course_syllabus',
            field=models.CharField(default='', max_length=800),
        ),
        migrations.AlterField(
            model_name='course',
            name='description',
            field=models.CharField(default='', max_length=800),
        ),
        migrations.AlterField(
            model_name='course',
            name='drop_consent',
            field=models.CharField(default='', max_length=32),
        ),
        migrations.AlterField(
            model_name='course',
            name='enroll_requirement',
            field=models.CharField(default='', max_length=300),
        ),
        migrations.AlterField(
            model_name='course',
            name='feedback',
            field=models.CharField(default='', max_length=800),
        ),
        migrations.AlterField(
            model_name='course',
            name='grading_basis',
            field=models.CharField(default='', max_length=32),
        ),
        migrations.AlterField(
            model_name='course',
            name='learning_outcome',
            field=models.CharField(default='', max_length=800),
        ),
        migrations.AlterField(
            model_name='course',
            name='recommended_reading',
            field=models.CharField(default='', max_length=800),
        ),
        migrations.AlterField(
            model_name='course',
            name='required_reading',
            field=models.CharField(default='', max_length=800),
        ),
        migrations.AlterField(
            model_name='course',
            name='units',
            field=models.FloatField(default=0),
        ),
    ]
