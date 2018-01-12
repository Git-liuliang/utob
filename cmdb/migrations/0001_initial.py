# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-01-10 06:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='userinfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('username', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=50)),
                ('createtime', models.DateTimeField()),
            ],
        ),
    ]