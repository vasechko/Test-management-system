# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-16 20:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('diplom', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='testrunresult',
            name='id',
        ),
        migrations.AlterField(
            model_name='testrunresult',
            name='testrunTestcase',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='diplom.TestRunTestCase'),
        ),
    ]
