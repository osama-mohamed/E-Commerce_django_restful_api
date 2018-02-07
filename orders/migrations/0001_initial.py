# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-01-29 06:58
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Checkout',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(default=b'pending', max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('price', models.PositiveIntegerField()),
                ('quantity', models.PositiveIntegerField()),
                ('discount', models.FloatField(blank=True, default=0, null=True)),
                ('image', models.ImageField(upload_to=b'')),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]