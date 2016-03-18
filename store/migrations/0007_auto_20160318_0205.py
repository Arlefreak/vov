# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-18 02:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_auto_20160318_0138'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductVariant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField(db_index=True, editable=False)),
                ('name', models.CharField(default='', max_length=140, verbose_name='Name')),
                ('sku', models.SlugField(editable=False, unique=True, verbose_name='SKU')),
                ('inventory', models.IntegerField(default=0, verbose_name='Inventory')),
            ],
            options={
                'ordering': ('order',),
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='product',
            name='inventory',
        ),
        migrations.RemoveField(
            model_name='product',
            name='url',
        ),
        migrations.AddField(
            model_name='productvariant',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.Product'),
        ),
    ]