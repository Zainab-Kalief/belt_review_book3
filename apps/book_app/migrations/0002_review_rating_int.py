# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-07-26 01:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='rating_int',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
    ]
