# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-01-25 13:22
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecomapp', '0008_auto_20190125_1351'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Brand',
            new_name='Author',
        ),
    ]
