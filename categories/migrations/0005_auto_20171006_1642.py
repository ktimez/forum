# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-06 16:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0004_auto_20171006_1640'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='subject',
            field=models.TextField(max_length=1000),
        ),
    ]
