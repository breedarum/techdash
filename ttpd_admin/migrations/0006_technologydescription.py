# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-09-15 00:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import ttpd_admin.models


class Migration(migrations.Migration):

    dependencies = [
        ('ttpd_admin', '0005_technologydescriptiontypes'),
    ]

    operations = [
        migrations.CreateModel(
            name='TechnologyDescription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.FileField(blank=True, upload_to=ttpd_admin.models.technology_description_path)),
                ('description_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ttpd_admin.TechnologyDescriptionTypes')),
                ('technology', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fulldescription', to='ttpd_admin.Technologies')),
            ],
            options={
                'verbose_name': 'technology description',
                'verbose_name_plural': 'technology description',
            },
        ),
    ]
