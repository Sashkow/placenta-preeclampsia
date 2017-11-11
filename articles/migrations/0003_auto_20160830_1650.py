# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-08-30 13:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0002_test'),
    ]

    operations = [
        migrations.CreateModel(
            name='OldSampleAttributeValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='OldSamplesAttributeName',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('experiment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='articles.Experiment')),
            ],
        ),
        migrations.CreateModel(
            name='SampleAttributeValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='SamplesAttributeNameInExperiment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='StandardName',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('mesh_id', models.CharField(blank=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='StandardValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=255)),
                ('mesh_id', models.CharField(blank=True, max_length=255)),
            ],
        ),
        migrations.RemoveField(
            model_name='test',
            name='microarrays',
        ),
        migrations.RemoveField(
            model_name='sample',
            name='data',
        ),
        migrations.DeleteModel(
            name='Test',
        ),
        migrations.AddField(
            model_name='samplesattributenameinexperiment',
            name='unificated_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='articles.StandardName'),
        ),
        migrations.AddField(
            model_name='sampleattributevalue',
            name='sample',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='articles.Sample'),
        ),
        migrations.AddField(
            model_name='sampleattributevalue',
            name='unificated_value',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='articles.StandardValue'),
        ),
        migrations.AddField(
            model_name='oldsampleattributevalue',
            name='sample',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='articles.Sample'),
        ),
        migrations.AddField(
            model_name='experiment',
            name='sample_attribute_names',
            field=models.ManyToManyField(to='articles.SamplesAttributeNameInExperiment'),
        ),
    ]
