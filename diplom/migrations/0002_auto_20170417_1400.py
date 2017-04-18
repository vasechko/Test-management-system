# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-17 12:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('diplom', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Priority',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='TestProject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('creation_date', models.DateTimeField()),
                ('modification_date', models.DateTimeField()),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='diplom.Status')),
            ],
        ),
        migrations.CreateModel(
            name='TestRun',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('testProject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='diplom.TestProject')),
            ],
        ),
        migrations.CreateModel(
            name='TestSuit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='diplom.TestProject')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=255)),
                ('email_address', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=255)),
            ],
        ),
        migrations.RemoveField(
            model_name='testcase',
            name='title',
        ),
        migrations.AddField(
            model_name='testcase',
            name='estimate',
            field=models.CharField(default='1m', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='testcase',
            name='precondition',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='testproject',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='diplom.User'),
        ),
        migrations.AddField(
            model_name='testcase',
            name='priority',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='diplom.Priority'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='testcase',
            name='testSuit',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='diplom.TestSuit'),
            preserve_default=False,
        ),
    ]