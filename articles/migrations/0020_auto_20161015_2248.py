# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-10-15 19:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0019_historicalexperiment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sampleattribute',
            name='old_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='sampleattribute',
            name='old_value',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]