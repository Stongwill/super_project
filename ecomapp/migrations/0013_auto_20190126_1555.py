# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-01-26 13:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecomapp', '0012_auto_20190126_1539'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='brand',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecomapp.Author', verbose_name='Автор'),
        ),
    ]
