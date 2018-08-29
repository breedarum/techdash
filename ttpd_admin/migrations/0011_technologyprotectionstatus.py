# Generated by Django 2.0.6 on 2018-08-28 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ttpd_admin', '0010_auto_20180827_2044'),
    ]

    operations = [
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
    ]