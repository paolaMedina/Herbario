# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-04-20 19:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('especimen', '0002_auto_20180416_1015'),
    ]

    operations = [
        migrations.AddField(
            model_name='especimen',
            name='visible',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='especimen',
            name='imagen',
            field=models.ImageField(blank=True, null=True, upload_to='fotografias/'),
        ),
    ]