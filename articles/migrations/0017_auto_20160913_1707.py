# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-09-13 14:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0016_unificatedsamplesattributename_synonyms'),
    ]

    operations = [
        migrations.AlterField(
            model_name='standardname',
            name='synonyms',
            field=models.ManyToManyField(related_name='_unificatedsamplesattributename_synonyms_+', to='articles.StandardName'),
        ),
    ]
