# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-09-15 00:31
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ttpd_admin', '0006_technologydescription'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TechnologyDescription',
            new_name='TechnologyFullDescription',
        ),
        migrations.RenameModel(
            old_name='TechnologyDescriptionTypes',
            new_name='TechnologyFullDescriptionTypes',
        ),
    ]