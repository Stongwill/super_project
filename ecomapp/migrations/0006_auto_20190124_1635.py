# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2019-01-24 16:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecomapp', '0005_auto_20190123_1602'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='buying_type',
            field=models.CharField(choices=[('\u0421\u0430\u043c\u043e\u0432\u044b\u0432\u043e\u0437', '\u0421\u0430\u043c\u043e\u0432\u044b\u0432\u043e\u0437'), ('\u0414\u043e\u0441\u0442\u0430\u0432\u043a\u0430', '\u0414\u043e\u0441\u0442\u0430\u0432\u043a\u0430')], default='\u0421\u0430\u043c\u043e\u0432\u044b\u0432\u043e\u0437', max_length=40, verbose_name='\u0422\u0438\u043f \u0437\u0430\u043a\u0430\u0437\u0430'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('\u041f\u0440\u0438\u043d\u044f\u0442 \u0432 \u043e\u0431\u0440\u0430\u0431\u043e\u0442\u043a\u0443', '\u041f\u0440\u0438\u043d\u044f\u0442 \u0432 \u043e\u0431\u0440\u0430\u0431\u043e\u0442\u043a\u0443'), ('\u0412\u044b\u043f\u043e\u043b\u043d\u044f\u0435\u0442\u0441\u044f', '\u0412\u044b\u043f\u043e\u043b\u043d\u044f\u0435\u0442\u0441\u044f'), ('\u041e\u043f\u043b\u0430\u0447\u0435\u043d', '\u041e\u043f\u043b\u0430\u0447\u0435\u043d')], default='\u041f\u0440\u0438\u043d\u044f\u0442 \u0432 \u043e\u0431\u0440\u0430\u0431\u043e\u0442\u043a\u0443', max_length=100, verbose_name='\u0421\u0442\u0430\u0442\u0443\u0441'),
        ),
    ]
