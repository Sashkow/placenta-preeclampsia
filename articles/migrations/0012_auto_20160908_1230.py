# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-09-08 09:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0011_auto_20160907_2247'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sampleattribute',
            name='unificated_name',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='articles.SamplesAttributeNameInExperiment'),
        ),
        migrations.AlterField(
            model_name='sampleattribute',
            name='unificated_value',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='articles.UnificatedSamplesAttributeValue'),
        ),
        migrations.AlterField(
            model_name='samplesattributenameinexperiment',
            name='unificated_name',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='articles.UnificatedSamplesAttributeName'),
        ),
    ]
