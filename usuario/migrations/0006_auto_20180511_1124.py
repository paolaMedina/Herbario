# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-05-11 16:24
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0005_auto_20180510_2244'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='usuario',
            options={'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='activation_key',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='key_expires',
        ),
    ]
