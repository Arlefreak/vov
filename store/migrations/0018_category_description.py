# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-29 04:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0017_auto_20160329_0343'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='description',
            field=models.TextField(blank=True, default='', verbose_name='Description'),
        ),
    ]
