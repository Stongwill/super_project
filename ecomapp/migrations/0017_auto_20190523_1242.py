# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-05-23 09:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecomapp', '0016_auto_20190523_1238'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='brand',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecomapp.Author', verbose_name='Автор'),
        ),
    ]
