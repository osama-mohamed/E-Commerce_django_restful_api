# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-01-26 09:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='number_of_products',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]