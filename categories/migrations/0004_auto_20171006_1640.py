# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-06 16:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0003_auto_20171006_1629'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reply',
            name='message',
            field=models.TextField(max_length=40000, null=True),
        ),
    ]