# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-09-04 01:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ttpd_admin', '0004_auto_20180903_1144'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='fundings',
            options={'verbose_name': 'funding', 'verbose_name_plural': 'fundings'},
        ),
        migrations.AlterModelOptions(
            name='fundingtypes',
            options={'verbose_name': 'technology funding type', 'verbose_name_plural': 'technology funding types'},
        ),
        migrations.AlterField(
            model_name='generators',
            name='title',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]