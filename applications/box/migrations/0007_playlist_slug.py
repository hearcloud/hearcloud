# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-08-21 23:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('box', '0006_auto_20160821_2312'),
    ]

    operations = [
        migrations.AddField(
            model_name='playlist',
            name='slug',
            field=models.SlugField(default='mi-playlist', unique=True, verbose_name='Slug'),
            preserve_default=False,
        ),
    ]
