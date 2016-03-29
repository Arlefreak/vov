# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-29 01:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0013_stores_publish'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stores',
            name='adress',
            field=models.CharField(blank=True, default='', max_length=500, verbose_name='Adress'),
        ),
        migrations.AlterField(
            model_name='stores',
            name='mail',
            field=models.EmailField(blank=True, default='', max_length=254, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='stores',
            name='notes',
            field=models.CharField(blank=True, default='', max_length=500, verbose_name='Notes'),
        ),
        migrations.AlterField(
            model_name='stores',
            name='phone',
            field=models.CharField(blank=True, default='', max_length=140, verbose_name='Phone'),
        ),
    ]
