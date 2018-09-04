# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-09-01 07:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ttpd_admin', '0002_auto_20180830_1152'),
    ]

    operations = [
        migrations.AddField(
            model_name='technologyadopters',
            name='break_even_point',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='technologyadopters',
            name='expected_returns',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='technologyadopters',
            name='financial_analysis',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='technologyadopters',
            name='internal_rate_return',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='technologyadopters',
            name='investment_cost',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='technologyadopters',
            name='net_present_value',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]