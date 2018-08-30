# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-08-30 03:52
from __future__ import unicode_literals

import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
        ('ttpd_admin', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FundingImplementors',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'technology funding implementor',
                'verbose_name_plural': 'technology funding implementors',
            },
        ),
        migrations.CreateModel(
            name='Fundings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('investment_amount', models.PositiveIntegerField(blank=True)),
                ('duration_start', models.DateField(blank=True)),
                ('duration_end', models.DateField(blank=True)),
                ('properties', models.TextField(blank=True)),
            ],
            options={
                'verbose_name': 'technology funding',
                'verbose_name_plural': 'technology fundings',
            },
        ),
        migrations.CreateModel(
            name='FundingTypes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'funding type',
                'verbose_name_plural': 'funding types',
            },
        ),
        migrations.CreateModel(
            name='Regions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
                ('region_roman', models.CharField(max_length=80)),
                ('region_canonical', models.CharField(max_length=160)),
            ],
            options={
                'verbose_name': 'region',
                'verbose_name_plural': 'regions',
            },
        ),
        migrations.CreateModel(
            name='TechCategories',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ttpd_admin.TechCategories')),
            ],
            options={
                'verbose_name': 'technology category',
                'verbose_name_plural': 'technology categories',
            },
        ),
        migrations.CreateModel(
            name='Technologies',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('year', models.CharField(blank=True, max_length=5, null=True)),
                ('description', models.TextField()),
                ('est_ownership_cost', models.PositiveIntegerField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'technology',
                'verbose_name_plural': 'technologies',
            },
        ),
        migrations.CreateModel(
            name='TechnologyAdopters',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'technology adopter',
                'verbose_name_plural': 'technology adopters',
            },
        ),
        migrations.CreateModel(
            name='TechnologyCategories',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tech_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ttpd_admin.TechCategories')),
                ('technology', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ttpd_admin.Technologies')),
            ],
            options={
                'verbose_name': 'technology category',
                'verbose_name_plural': 'technology categories',
            },
        ),
        migrations.CreateModel(
            name='TechnologyCommodities',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('commodity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ttpd_admin.Commodities')),
                ('technology', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ttpd_admin.Technologies')),
            ],
            options={
                'verbose_name': 'technology commodity',
                'verbose_name_plural': 'technology commodities',
            },
        ),
        migrations.CreateModel(
            name='TechnologyGenerators',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'technology generators',
                'verbose_name_plural': 'technology generators',
            },
        ),
        migrations.CreateModel(
            name='TechnologyIndustrySectorISPs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'technology isp',
                'verbose_name_plural': 'technology isps',
            },
        ),
        migrations.CreateModel(
            name='TechnologyOwners',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'technology owner',
                'verbose_name_plural': 'technology owners',
            },
        ),
        migrations.CreateModel(
            name='TechnologyPotentialAdopters',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('potential_adopter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ttpd_admin.PotentialAdopters')),
                ('technology', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ttpd_admin.Technologies')),
            ],
            options={
                'verbose_name': 'technology potential adopter',
                'verbose_name_plural': 'technology potential adopters',
            },
        ),
        migrations.CreateModel(
            name='TechnologyProtectionStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'technology protection status',
                'verbose_name_plural': 'technology protection statuses',
            },
        ),
        migrations.CreateModel(
            name='TechnologyProtectionTypes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('protection_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ttpd_admin.ProtectionTypes')),
            ],
            options={
                'verbose_name': 'technology protection type',
                'verbose_name_plural': 'technology protection types',
            },
        ),
        migrations.CreateModel(
            name='TechnologyStatuses',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year_complied', models.CharField(blank=True, max_length=5)),
                ('tech_status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ttpd_admin.TechStatus')),
                ('technology', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ttpd_admin.Technologies')),
            ],
            options={
                'verbose_name': 'technology status',
                'verbose_name_plural': 'technology statuses',
            },
        ),
        migrations.CreateModel(
            name='TechProtectionTypesMetadata',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('application_number', models.CharField(blank=True, max_length=255)),
                ('meta_serial_number', models.CharField(blank=True, max_length=255)),
                ('date_of_filing', models.DateField(blank=True)),
                ('status', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='ttpd_admin.TechnologyProtectionStatus')),
            ],
            options={
                'verbose_name': 'technology protection type metadata',
                'verbose_name_plural': 'technology protection type metadatas',
            },
        ),
        migrations.RemoveField(
            model_name='specificcommodities',
            name='parent',
        ),
        migrations.CreateModel(
            name='User',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AlterModelOptions(
            name='adopters',
            options={'verbose_name': 'adopter', 'verbose_name_plural': 'adopters'},
        ),
        migrations.AddField(
            model_name='agencies',
            name='private_flag',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='isps',
            name='specific_commodity',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ttpd_admin.ISPs'),
        ),
        migrations.AlterField(
            model_name='adopters',
            name='fax_number',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='agencies',
            name='fax_number',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='generators',
            name='agency',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ttpd_admin.Agencies'),
        ),
        migrations.AlterField(
            model_name='generators',
            name='title',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.DeleteModel(
            name='SpecificCommodities',
        ),
        migrations.AddField(
            model_name='technologyprotectiontypes',
            name='protection_type_meta',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ttpd_admin.TechProtectionTypesMetadata'),
        ),
        migrations.AddField(
            model_name='technologyprotectiontypes',
            name='technology',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ttpd_admin.Technologies'),
        ),
        migrations.AddField(
            model_name='technologyowners',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ttpd_admin.Agencies'),
        ),
        migrations.AddField(
            model_name='technologyowners',
            name='technology',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ttpd_admin.Technologies'),
        ),
        migrations.AddField(
            model_name='technologyindustrysectorisps',
            name='industry_sector_isp',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ttpd_admin.ISPs'),
        ),
        migrations.AddField(
            model_name='technologyindustrysectorisps',
            name='technology',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ttpd_admin.Technologies'),
        ),
        migrations.AddField(
            model_name='technologygenerators',
            name='generator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ttpd_admin.Generators'),
        ),
        migrations.AddField(
            model_name='technologygenerators',
            name='technology',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ttpd_admin.Technologies'),
        ),
        migrations.AddField(
            model_name='technologyadopters',
            name='adopter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ttpd_admin.Adopters'),
        ),
        migrations.AddField(
            model_name='technologyadopters',
            name='technology',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ttpd_admin.Technologies'),
        ),
        migrations.AddField(
            model_name='technologies',
            name='adopters',
            field=models.ManyToManyField(blank=True, through='ttpd_admin.TechnologyAdopters', to='ttpd_admin.Adopters'),
        ),
        migrations.AddField(
            model_name='technologies',
            name='categories',
            field=models.ManyToManyField(through='ttpd_admin.TechnologyCategories', to='ttpd_admin.TechCategories'),
        ),
        migrations.AddField(
            model_name='technologies',
            name='commodities',
            field=models.ManyToManyField(through='ttpd_admin.TechnologyCommodities', to='ttpd_admin.Commodities'),
        ),
        migrations.AddField(
            model_name='technologies',
            name='generators',
            field=models.ManyToManyField(blank=True, through='ttpd_admin.TechnologyGenerators', to='ttpd_admin.Generators'),
        ),
        migrations.AddField(
            model_name='technologies',
            name='industry_sector_isp',
            field=models.ManyToManyField(through='ttpd_admin.TechnologyIndustrySectorISPs', to='ttpd_admin.ISPs'),
        ),
        migrations.AddField(
            model_name='technologies',
            name='owners',
            field=models.ManyToManyField(blank=True, through='ttpd_admin.TechnologyOwners', to='ttpd_admin.Agencies'),
        ),
        migrations.AddField(
            model_name='technologies',
            name='potential_adopters',
            field=models.ManyToManyField(blank=True, through='ttpd_admin.TechnologyPotentialAdopters', to='ttpd_admin.PotentialAdopters'),
        ),
        migrations.AddField(
            model_name='technologies',
            name='protection_level',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ttpd_admin.ProtectionLevels'),
        ),
        migrations.AddField(
            model_name='technologies',
            name='protection_types',
            field=models.ManyToManyField(blank=True, through='ttpd_admin.TechnologyProtectionTypes', to='ttpd_admin.ProtectionTypes'),
        ),
        migrations.AddField(
            model_name='technologies',
            name='region',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ttpd_admin.Regions'),
        ),
        migrations.AddField(
            model_name='technologies',
            name='statuses',
            field=models.ManyToManyField(blank=True, through='ttpd_admin.TechnologyStatuses', to='ttpd_admin.TechStatus'),
        ),
        migrations.AddField(
            model_name='fundings',
            name='donor',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='fundings', to='ttpd_admin.Agencies'),
        ),
        migrations.AddField(
            model_name='fundings',
            name='funding_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ttpd_admin.FundingTypes'),
        ),
        migrations.AddField(
            model_name='fundings',
            name='implementing_agencies',
            field=models.ManyToManyField(blank=True, related_name='funding_implementations', through='ttpd_admin.FundingImplementors', to='ttpd_admin.Agencies'),
        ),
        migrations.AddField(
            model_name='fundings',
            name='technology',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fundings', to='ttpd_admin.Technologies'),
        ),
        migrations.AddField(
            model_name='fundingimplementors',
            name='funding',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ttpd_admin.Fundings'),
        ),
        migrations.AddField(
            model_name='fundingimplementors',
            name='implementor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ttpd_admin.Agencies'),
        ),
    ]
