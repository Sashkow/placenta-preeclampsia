# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-09-06 11:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0007_auto_20160831_1901'),
    ]

    operations = [
        migrations.CreateModel(
            name='UnificatedSamplesAttributeName',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('mesh_id', models.CharField(blank=True, max_length=255)),
            ],
        ),
        migrations.RenameField(
            model_name='sampleattributevalueinsample',
            old_name='unificated_value',
            new_name='unificated_name_value',
        ),
        migrations.AddField(
            model_name='samplesattributenameinexperiment',
            name='unificated_name',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='articles.UnificatedSamplesAttributeName'),
            preserve_default=False,
        ),
    ]