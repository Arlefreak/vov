# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-18 02:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_auto_20160318_0205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productimages',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.ProductVariant'),
        ),
    ]
